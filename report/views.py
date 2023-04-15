from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from association.models import Association
from auths.models import Role, Staff

from core.models import Region
from core.views import delete_files_in_dir
from market import models as market_models
from ninja.errors import HttpError
from .forms import *
from core.models import Region, GradePrice, CropGrade, Season
from market.models import Market as market_table
from shipment.models import MarketWarehouseShipmentBale,GeneralShipmentBale
from market.views import PrintRequest as print_request_class
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.views.generic import CreateView,ListView,UpdateView,View,FormView,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import (
    IntegerField,
    FloatField,
    F,
    Sum,
    Value,
    When,
    Case,
    Count,
    Q,
    Min,
    Max,
)
from django.contrib import messages
from core.common import common_render_to_pdf
from report.report_functions import *
from core.common import common_render_to_pdf


class MarketDeclaration:
    def __init__(self):
        pass

    @login_required(login_url="/login")
    def get_sale_no(request):
        nos = market_models.MarketTicketRequest.objects.filter(
            market_id=request.GET.get("market"), society_id=request.GET.get("society")
        ).order_by("-created_on")
        html = ""
        for n in nos:
            html += (
                '<option value"'
                + str(n.sales_number)
                + '">'
                + str(n.sales_number)
                + "</option>"
            )
        return HttpResponse(html)

    @login_required(login_url="/login")
    def get_market_declaration(request):
        form = PcnReportForm(request.POST or None)
        template_name = "report/declaration/dec_form.html"
        if request.method == "POST":
            form = PcnReportForm(request.POST or None)
            if not form.is_valid():
                print(form.errors)
                return render(request, template_name, {"form": form})
            else:
                season = request.POST.get("season")
                saleno = request.POST.get("sale_no")
                market = request.POST.get("market")
                society = request.POST.get("primary_society")
                post_type = request.POST.get("post_type")
                req = market_models.MarketTicketRequest.objects.filter(
                    society=society,
                    market_id=market,
                    sales_number=saleno,
                    season=season,
                ).first()

                pcn = market_declaration_list(society, market, saleno, season)
                pcn_total = market_declaration_total(society, market, saleno, season)

                header = (
                    market_models.Market.objects.get(
                        id=request.POST.get("market")
                    ).market_name
                    + " DECLARATION REPORT "
                )
                if "pdf" in post_type:
                    context = {}
                    context["req"] = market_models.MarketTicketRequest.objects.filter(
                        society=society,
                        market_id=market,
                        sales_number=saleno,
                        season_id=season,
                    ).first()
                    context["pcns"] =data= market_declaration_list_empty(
                        society, market, saleno, season
                    )
                    #return HttpResponse(data.count())
                    context["pcns_total"] = market_declaration_total_empty(
                        society, market, saleno, season
                    )
                    context["header"] = (
                        market_models.Market.objects.get(id=market).market_name
                        + " DECLARATION REPORT "
                    )

                    soc = market_models.Market.objects.get(id=market).market_name
                    context["user"] = request.user
                    context["date"] = datetime.today().now()

                    # return HttpResponse(pcn)
                    pdf = common_render_to_pdf(
                        "report/declaration/pdf/dec_empty_pdf.html", context, "file"
                    )
                    if pdf:

                        response = HttpResponse(
                            pdf, content_type="application/force-download"
                        )
                        content = "attachment; filename=%s.pdf  " % soc
                        response["Content-Disposition"] = content
                        return response
                    else:
                        return HttpResponse("Not found")
                return render(
                    request,
                    "report/declaration/list.html",
                    {
                        "pcns": pcn,
                        "pcns_total": pcn_total,
                        "society": society,
                        "market": market,
                        "sale_no": saleno,
                        "header": header,
                        "req": req,
                    },
                )
        return render(request, template_name, {"form": form, "header": ""})

    @login_required(login_url="/login")
    def get_declaration_data_pdf(request):
        template_name = "report/declaration/pdf/dec_data_pdf.html"
        context_object_name = "lists"
        saleno = request.GET.get("sale_no")
        market = request.GET.get("market")
        society = request.GET.get("society")
        season = request.GET.get("season")
        context = {}
        context["req"] = market_models.MarketTicketRequest.objects.filter(
            society=society, market_id=market, sales_number=saleno, season_id=season
        ).first()
        context["pcns"] = market_declaration_list(society, market, saleno, season)
        context["pcns_total"] = market_declaration_total(
            society, market, saleno, season
        )
        market = market_models.Market.objects.get(id=market)
        context["header"] = market.market_name + " DECLARATION REPORT "

        soc = market.market_name
        context["user"] = request.user
        context["date"] = datetime.today().now()

        # return HttpResponse(pcn)
        pdf = common_render_to_pdf(template_name, context, "file")
        if pdf:

            response = HttpResponse(pdf, content_type="application/force-download")
            content = "attachment; filename=%s.pdf  " % soc
            response["Content-Disposition"] = content
            return response
        else:
            return HttpResponse("Not found")


class SaleReport:
    @login_required(login_url="/login")
    def society_market_sale_report(request):
        header = "SOCIETY SALE SUMMARY REPORT"
        form = PcnReportForm(request.POST or None)
        if form.is_valid():
            saleno = request.POST.get("sale_no")
            market = request.POST.get("market")
            season = request.POST.get("season")
            society = request.POST.get("primary_society")
            req = market_models.MarketTicketRequest.objects.filter(
                society_id=society,
                market_id=market,
                sales_number=saleno,
                season_id=season,
            ).first()
            pcn = single_society_market_report_list(society, market, saleno, season)
            pcns_total = single_society_market_report_total(
                society, market, saleno, season
            )

            return render(
                request,
                "report/society-sale/list.html",
                {
                    "pcns": pcn,
                    "header": header,
                    "pcns_total": pcns_total,
                    "req": req,
                    "society": society,
                    "market": market,
                    "sale_no": saleno,
                },
            )

        return render(
            request,
            "report/society-sale/society_sale_report_form.html",
            {"form": form, "header": header},
        )
    @login_required(login_url="/login")
    def society_market_sale_report_pdf(request):
        saleno = request.GET.get("sale_no")
        market = request.GET.get("market")
        society = request.GET.get("society")
        season = request.GET.get("season")
        template_name = "report/society-sale/pdf/society_sale_report_pdf.html"
        context = {}
        context["req"] = market_models.MarketTicketRequest.objects.filter(
            society=society, market_id=market, sales_number=saleno, season=season
        ).first()
        context["pcns"] = single_society_market_report_list(
            society, market, saleno, season
        )
        context["pcns_total"] = single_society_market_report_total(
            society, market, saleno, season
        )
        societyob = Association.objects.get(id=society)
        context["header"] = societyob.name + " SUMMARY REPORT "

        soc = societyob.name
        context["header"] = header = societyob.name + " " + " SUMMARY REPORT "
        context["user"] = request.user
        context["date"] = datetime.today().now()
        # return HttpResponse(pcn)
        pdf = common_render_to_pdf(template_name, context, "file")
        if pdf:

            response = HttpResponse(pdf, content_type="application/force-download")
            content = "attachment; filename=%s.pdf  " % soc
            response["Content-Disposition"] = content
            return response
        else:
            return HttpResponse("Not found")


class PaidReport:
    @login_required(login_url="/login")
    def society_paid_report(request):
        header = "SOCIETY PAID REPORT"
        form = PerSocietyReportForm(request.POST or None)
        if form.is_valid():
            season = request.POST.get("season")
            society = request.POST.get("primary_society")
            pcn = single_society_sale_list(society, season)
            pcns_total = single_society_sale_total(society, season)

            header = (
                Association.objects.get(id=society).name
            ).upper() + " PAID REPORT "
            return render(
                request,
                "report/society-paid/society_paid_list.html",
                {
                    "pcns": pcn,
                    "header": header,
                    "pcns_total": pcns_total,
                    "year_id": season,
                    "society": society,
                },
            )
        return render(
            request,
            "report/society-paid/society_paid_form.html",
            {"form": form, "header": header},
        )
    @login_required(login_url="/login")
    def society_paid_report_pdf(request):
        context = {}
        context["season"] = season = request.GET.get("year")
        context["society"] = society = request.GET.get("society")
        context["pcns"] = pcn = single_society_sale_list(society, season)
        context["pcns_total"] = pcns_total = single_society_sale_total(society, season)
        context["user"] = request.user
        context["date"] = datetime.today().now()
        context["societyname"] = societyname = (
            Association.objects.get(id=society).name
        ).upper()
        context["header"] = header = (
            Season.objects.get(id=season).season_name + "  PAID REPORT "
        )
        # return HttpResponse(pcn)
        pdf = common_render_to_pdf(
            "report/society-paid/pdf/society_paid_report_pdf.html", context, "file"
        )
        if pdf:

            response = HttpResponse(pdf, content_type="application/force-download")
            content = "attachment; filename=%s.pdf  " % societyname
            response["Content-Disposition"] = content
            return response
        else:
            return HttpResponse("Not found")

    @login_required(login_url="/login")
    def region_paid_report(request):
        header = "REGION PAID REPORT"
        form = RegionalPaidReportForm(request.POST or None)
        if form.is_valid():
            season = request.POST.get("season")
            region = request.POST.get("region")
            pcn = reional_society_paid_list(region, season)
            pcns_total = regional_society_paid_total(region, season)
            # societies=Association.objects.filter(region_id=region)

            header = (
                Region.objects.get(id=region).region_name
            ).upper() + " PAID REPORT "
            return render(
                request,
                "report/society-paid/region_paid_list.html",
                {
                    "societies": pcn,
                    "header": header,
                    "pcns_total": pcns_total,
                    "year_id": season,
                    "region": region,
                },
            )

        return render(
            request,
            "report/society-paid/region_paid_form.html",
            {"form": form, "header": header},
        )

    @login_required(login_url="/login")
    def region_paid_report_pdf(request):
        context = {}
        template_name = "report/society-paid/pdf/region_paid_report_pdf.html"
        context["year_id"] = year = request.GET.get("season")
        context["region"] = region = request.GET.get("region")
        context["societies"] = reional_society_paid_list(region, year)
        context["regob"] = regob = Region.objects.get(id=region)

        context["pcns_total"] = regional_society_paid_total(region, year)

        context["header"] = (
            Region.objects.get(id=region).region_name
        ).upper() + " PAID REPORT "
        context["date"] = datetime.today().now()
        # return HttpResponse(pcn)
        pdf = common_render_to_pdf(template_name, context, "file")
        if pdf:

            response = HttpResponse(pdf, content_type="application/force-download")
            content = "attachment; filename=%s.pdf  " % regob.region_name
            response["Content-Disposition"] = content
            return response
        else:
            return HttpResponse("Not found")

class ReportViewGeneral:
    @login_required(login_url="/login")
    def current_buying_report(request):
        header = "TOTAL BUYING REPORT"
        form = VerifiedBuyingReportAll(request.POST or None)
        if form.is_valid():
            season = request.POST.get("season")
            allmarkets = current_buying_reports(season)
            allmarketstotal = current_buying_reports_total(season)
            
            return render(
                request,
                "report/managers/buying_report.html",
                {
                    "societies": allmarkets,
                    "header": header,
                    "pcns_total": allmarketstotal,
                    "year_id": season,
                },
            )

        return render(
            request,
            "report/managers/verified_buying_report_form.html",
            {"form": form, "header": header},
        )
    @login_required(login_url="/login")
    def analysed_buying_report(request):
        header = "VERIFIED BUYING REPORT"
        form = VerifiedBuyingReportAll(request.POST or None)
        if form.is_valid():
            season = request.POST.get("season")
            allmarkets = warehouse_verified_buying_reports(season)
            allmarketstotal = warehouse_verified_buying_reports_total(season)
            
            return render(
                request,
                "report/managers/verified_buying_report.html",
                {
                    "societies": allmarkets,
                    "header": header,
                    "pcns_total": allmarketstotal,
                    "year_id": season,
                },
            )

        return render(
            request,
            "report/managers/verified_buying_report_form.html",
            {"form": form, "header": header},
        )

    @login_required(login_url="/login")
    def analysed_buying_report_buyer_summary(request):
        header = "BUYING BUYER SUMMARY"
        form = VerifiedBuyingReportAll(request.POST or None)
        if form.is_valid():
            season = request.POST.get("season")
            allmarkets = warehouse_verified_buying_reports_buyersummary(season)
            #allmarketstotal = warehouse_verified_buying_reports_total_buyersummary(season)
            
            return render(
                request,
                "report/managers/buyersummary_buying_report.html",
                {
                    "societies": allmarkets,
                    "header": header,
                    "pcns_total": allmarkets,
                    "year_id": season,
                },
            )

        return render(
            request,
            "report/managers/verified_buying_report_form.html",
            {"form": form, "header": header},
        )

    @login_required(login_url="/login")
    def analysed_buying_report_per_buyer(request):
        header = "VERIFIED BUYING BUYER REPORT"
        form = VerifiedBuyingReportPerBuyer(request.POST or None)
        if form.is_valid():
            season = request.POST.get("season")
            buyer = request.POST.get("buyer")
            buyerob=market_models.Buyer.objects.get(id=buyer)
            allmarkets = warehouse_verified_buying_reports_per_buyer(season,buyerob.buyer_code)
            allmarketstotal = warehouse_verified_buying_reports_total_per_buyer(season,buyerob.buyer_code)
            
            return render(
                request,
                "report/managers/verified_buying_report_per_buyer.html",
                {
                    "societies": allmarkets,
                    "buyer_code":buyerob.buyer_code,
                    "header": buyerob.full_name+' ('+ buyerob.buyer_code+' ) BUYING REPORT',
                    "pcns_total": allmarketstotal,
                    "year_id": season,
                },
            )

        return render(
            request,
            "report/managers/verified_buying_report_form_per_buyer.html",
            {"form": form, "header": header},
        )

    @login_required(login_url="/login")
    def shipping_report(request):
        header = "SHIPPING REPORT"
        context={}
        context['header']=header
        context['totals']=GeneralShipmentBale.objects.filter(general_shipment__is_closed_transporting=True).aggregate(bls=Count('id'),summ=Sum('transport_weight'))
        context['summaries']=GeneralShipmentBale.objects.filter(general_shipment__is_closed_transporting=True).values(fromw=F('general_shipment__from_warehouse__warehouse_name'),tow=F('general_shipment__to_warehouse__warehouse_name'),shipmentno=F('general_shipment__shipment_number'),gid=F('general_shipment_id')).annotate(bls=Count('id'),summ=Sum('transport_weight')).order_by('general_shipment__created_on')
        return render(request,"report/managers/shipping_summary_report.html",context)
    
    @login_required(login_url="/login")
    def shipped_value_report(request):
        """BOUGHT SHIPPED VALUES"""
        header = "SHIPPED VALUE REPORT"
        form = VerifiedBuyingReportAll(request.POST or None)
        if form.is_valid():
            season = request.POST.get("season")
            allmarkets = shipped_value_comparison_report(season,'all')
            totaallmarkets=shipped_value_comparison_report_total(season,'all')
            #allmarketstotal = warehouse_verified_buying_reports_total_buyersummary(season)
            
            return render(
                request,
                "report/managers/sold/shipped_bought_reports.html",
                {
                    "totals": totaallmarkets,
                    "header": header,
                    "shippedvalues": allmarkets,
                    "year_id": season,
                 },
            )

        return render(
            request,
            "report/managers/sold/shipped_bought_report_form.html",
            {"form": form, "header": header},
        )

    #####GRADE ANSlysis    
    @login_required(login_url="/login")
    def grade_analysis_yearly(request):
        """BOUGHT SHIPPED VALUES"""
        header = "GRADE ANALYSIS"
        form = RegionalAnalysiForm(request.POST or None)
        if form.is_valid():
            season = request.POST.get("season")
            region = request.POST.get("region")
            if region:
                region_name=Region.objects.get(id=region).region_name
            else:
                region_name='ALL REGIONS'

            seasonob=Season.objects.filter(id=season).first()
            allmarkets = grade_analysis_yearly(season,region)
            totaallmarkets=grade_analysis_yearly_total(season,region)
            #allmarketstotal = warehouse_verified_buying_reports_total_buyersummary(season)
            
            return render(
                request,
                "report/grade-analysis/list_all.html",
                {
                    "tickets": allmarkets,
                    "header":region_name+' '+ header+' ['+str(seasonob.season_name)+']',
                    "tickets_total": totaallmarkets,
                    "year_id": season,
                 },
            )

        return render(
            request,
            "report/grade-analysis/form.html",
            {"form": form, "header": header},
        )



#####################################################
#############
#####################################################
class ALLSocietyBuyingReportYealy(LoginRequiredMixin,CreateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = market_models.Pcn
    form_class=AllSocietyBuyingReport
    template_name = 'report/society-sale/society_buying_report_form.html'
    context_object_name = 'form'
    header='YEARLY SOCIETY BUYING  REPORT'

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            year=request.POST.get('season')
            pcn=allsociety_pcn_listsum_yearly(year)
            pcns_total=allsociety_pcn_total_yearly(year)
            header=Season.objects.get(id=year).season_name+ ' SOCIETIES BUYING SUMMARY '
            return  render(request,'report/society-sale/society_buying_sumary_report.html',{'pcns':pcn,'header':header,'pcns_total':pcns_total,'year_id':year})
        return  render(request,'report/society-sale/society_buying_report_form.html',{'form':form,'header':self.header})


#############PDF ALL SOCIETY SUMARY REPORTY
class ALLSocietySaleReportYealyPDF(LoginRequiredMixin,View):
    login_url = reverse_lazy('login-user')
    redirect_field_name = 'next'
    template_name = 'report/society-sale/pdf/sales_sum_pdf.html'
    context_object_name = 'lists'
    def get(self,request, *args, **kwargs):
        context={}
        context['year']= year=request.GET.get('year')
        context['pcn']=pcn=allsociety_pcn_listsum_yearly(year)
        context['pcns_total'] =  pcns_total=allsociety_pcn_total_yearly(year)
        context['header'] = header=Year.objects.get(id=year).year+ ' SOCIETIES SUMMARY REPORT '
        context['user']=request.user
        context['date']=datetime.today().now()
        pdf = render_to_pdf(self.template_name, context,'file')
        if pdf:

            response = HttpResponse(pdf, content_type='application/force-download')
            content = "attachment; filename=SOCIETIES YEARLY REPORT.pdf  "
            response['Content-Disposition'] = content
            return response
        else:
           return HttpResponse("Not found")

#########GRADE ANALYSIS
class ReportGradeAnalysisPerSociety(LoginRequiredMixin,CreateView):
    redirect_field_name = 'next'
    login_url = reverse_lazy('login_user')
    model = market_models.Pcn
    form_class=PerSocietyReportForm
    template_name = 'report/grade-analysis/society_grade_analysis_form.html'
    template_name2='report/grade-analysis/society_grade_analysis_list.html'
    context_object_name = 'form'
    header='SOCIETY GRADE ANALYSIS'

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']=self.header
        return context

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            year=request.POST.get('season')
            #market=request.POST.get('market')
            society=request.POST.get('primary_society')
            #saleno=request.POST.get('sale_no')

            tickets=grade_analysis_per_society(society,year)
            tickets_total=grade_analysis_per_society_total(society,year)

            
            header=' GRADE ANALYSIS ['+Association.objects.get(id=society).name+']'
            return  render(request,self.template_name2,{'year':year,'tickets':tickets,'header':header,'tickets_total':tickets_total,'year_id':year,'society':society})
        return  render(request,self.template_name,{'form':form,'header':self.header})
