import os
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from association.models import Association
from auths.models import Role, Staff
from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy
from core.models import Region
from core.views import delete_files_in_dir
from market import models as market_models
from ninja.errors import HttpError
from .forms import *
from core.models import Region, GradePrice, CropGrade, Season,InHouseGrade
from .models import Market as market_table
from market.models import Buyer as Buyer_table
from auths.models import Staff, User
from shipment.models import MarketWarehouseShipmentBale,GeneralShipmentBale,SendingShipmentEmail
from .views import PrintRequest as print_request_class
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from shipment.models import MarketWarehouseShipmentBale
from datetime import datetime

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
from market.pcn import create_pcn,create_pcn_for_additional
from core.common import common_render_to_pdf
from django.views.generic import CreateView,ListView,UpdateView,View,FormView,DeleteView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin



class Market:
    def __init__(self):
        pass

    @login_required(login_url="/login")
    def get_inactivemarkets(request):
        header='Inactive Markets'
        try:
            template_name = "market/market_list.html"
            markets = market_models.Market.objects.filter(is_active=False).order_by(
                "-created_on"
            )
            return render(request, template_name, {"markets": markets,'header':header})
        except:
            raise HttpError(500, "Internal Server Error")

    @login_required(login_url="/login")
    def get_markets(request):
        header = 'Markets'
        try:
            template_name = "market/market_list.html"
            markets = market_models.Market.objects.filter(is_active=True).order_by(
                "-created_on"
            )
            return render(request, template_name, {"markets": markets,'header':header})
        except:
            raise HttpError(500, "Internal Server Error")

    def delete_market(request, market_id):
        market = market_models.Market.objects.filter(id=market_id)
        if market.first().is_active:
            market.first().is_active=False
            messages.success(request,'Market deactivated')
        else:
            market.first().is_active = True
            messages.success(request, 'Market activated')
        market.first().save()
        return redirect("/market/market-list")

    @login_required(login_url="/login")
    def get_market_ticket_requests(request):
        # try:
        template_name = "market/market_print_request.html"
        market_ticket_requests = market_models.MarketTicketRequest.objects.filter(
            Q(is_active=True) & Q(Q(on_pre_buying=True)|Q(on_buying=True))
        ).order_by("-created_on")
        paginated_market_ticket_requests = Paginator(market_ticket_requests, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_market_ticket_requests.get_page(page_number)
        return render(
            request,
            template_name,
            {"page_obj": market_ticket_requests,'header':'CURRENT MARKETS'},
        )

    @login_required(login_url="/login")
    def get_market_ticket_requests_completed(request):
        # try:
        template_name = "market/market_print_request.html"
        market_ticket_requests = market_models.MarketTicketRequest.objects.filter(
            is_active=True,on_pre_buying=False,on_buying=False
        ).order_by("-created_on")
       
        return render(
            request,
            template_name,
            {"page_obj": market_ticket_requests,'header':'COMPLETED MARKETS'},
        )

    @login_required(login_url="/login")
    def market_ticket_list(request, request_id,wh=''):
        context = {}
        template_name = "market/market_request_tickets.html"
        context['wh']=request.GET.get('wh')
        #try:
        wh=request.GET.get('wh')
        if not wh:
            template_name = "market/market_request_tickets.html"
            context["bales"] = Bale.objects.filter(market_request_id=request_id).order_by(
            "ticket__no"
             )
        else:
            template_name = "market/mannual_ticket_list.html"
            context["bales"] = Bale.objects.filter(market_request_id=request_id,warehouse__warehouse_name__icontains=wh).order_by(
            "ticket__no"
             )
        if wh:

            context['datacaptured'] = (
                Bale.objects.filter(market_request_id=request_id,warehouse__warehouse_name__icontains=wh)
                .values("market_request_id")
                .annotate(
                    count=Count("id"),
                    countkg=Sum(
                        Case(
                            When(warehouse__warehouse_name__icontains="MSD", then='current_weight'),
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    ),
                    msd=Sum(
                        Case(
                            When(warehouse__warehouse_name__icontains="MSD", then=Value(1)),
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    ),
                    msdkg=Sum(
                        Case(
                            When(warehouse__warehouse_name__icontains="MSD", then='current_weight'),
                        ),
                        default=Value(0),
                        output_field=FloatField(),
                    ),
                    isaka=Sum(
                        Case(
                            When(warehouse__warehouse_name__icontains="ISAKA", then=Value(1)),
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    ),
                    isakakg=Sum(
                        Case(
                            When(warehouse__warehouse_name__icontains="ISAKA", then='current_weight'),
                        ),
                        default=Value(0),
                        output_field=FloatField(),
                    ),
                    nyuzi=Sum(
                        Case(
                            When(warehouse__warehouse_name__icontains="NYU", then=Value(1)),
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    ),
                    nyuzikg=Sum(
                        Case(
                            When(warehouse__warehouse_name__icontains="NYU", then='current_weight'),
                        ),
                        default=Value(0),
                        output_field=FloatField(),
                    )
                   
                )
            )

        context["market_request"] = MarketTicketRequest.objects.get(id=request_id)
        return render(request, template_name, context)
        # except:
        #    raise HttpError(500, "internal Server Error")

    def get_bales_by_request_id(request, request_id):
        template_name = "market/market_ticket_request_details.html"
        market_request = market_models.MarketTicketRequest.objects.get(id=request_id)
        # pcns = market_models.Pcn.objects.get(request_id=request_id)
        bales = market_models.Bale.objects.filter(
            ticket__id__in=[
                market_ticket.ticket.id
                for market_ticket in market_models.MarketTiket.objects.filter(
                    market_ticket_request__id=request_id
                )
            ]
        ).distinct("ticket__ticket_number")
        pcns = (
            Bale.objects.filter(pcn__request_id=request_id)
            .values(
                pcnn=F("pcn__pcn_no"),
                pcn_nid=F("pcn_id"),
                mname=F("market_request__market__market_name"),
                societyname=F("market_request__society__name"),
            ).annotate(
                count=Count("id"),
                verified=Sum(
                    Case(
                        When(pcn__is_data_verified=True, then=Value(1)),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
                problem=Sum(
                    Case(
                        When(
                            Q(grade__grade_name="C") | Q(grade__grade_name="R") | Q(grade__grade_name="W"), then=Value(1)
                        ),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            )
            .order_by("pcn__no")
        )
        datacaptured = (
            Bale.objects.filter(market_request_id=request_id)
            .values("market_request_id")
            .annotate(
                count=Count("id"),
                cancelled=Sum(
                    Case(
                        When(grade__grade_name="C", then=Value(1)),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
                rejected=Sum(
                    Case(
                        When(grade__grade_name="R", then=Value(1)),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
                withdrawn=Sum(
                    Case(
                        When(grade__grade_name="W", then=Value(1)),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
                prebuying=Sum(
                    Case(
                        When(
                            Q(primary_weight__isnull=False),
                            then=Value(1),
                        ),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
                buying=Sum(
                    Case(
                        When(
                            Q(primary_weight__isnull=False)
                            & Q(buyer_code__isnull=False)
                            & Q(grade_id__isnull=False),
                            then=Value(1),
                        ),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            )
        )
        paginated_bales = Paginator(bales, 10)
        page_number = request.GET.get("page")
        page_obj = None  # paginated_bales.get_page(page_number)
        return render(
            request,
            template_name,
            {
                "page_obj": page_obj,
                "market_request": market_request,
                "pcns": pcns,
                "datacaptured": datacaptured,
            },
        )

    @login_required(login_url="/login")
    def get_print_requests(request):
        try:
            template_name = "market/print_requests.html"
            market_ticket_requests = market_models.PrintRequest.objects.filter(
                is_active=True
            ).order_by("-created_on")
            paginated_print_requests = Paginator(market_ticket_requests, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_print_requests.get_page(page_number)
            return render(request, template_name, {"page_obj": page_obj})
        except:
            raise HttpError(500, "Internal Server Error")

    @login_required(login_url="/login")
    def old_ticket_to_locked(request):
        # try:
        lists = list(market_models.MarketTiket.objects.values_list('ticket_id', flat=True))
        tickets = None#Ticket.objects.filter(~Q(id__in=lists) & Q(no__gte=115000)).order_by('created_on')
        count = 0

        market_ticket_request = market_models.MarketTicketRequest.objects.get(id='ec50a15c-5361-4337-848b-3de73b183eab')
        # tickets=Ticket.objects.filter(id__in=lists).order_by('created_on')
        number_of_tickets = 29
        ticket_of = 0

        for ticket in tickets:
            ticket_of += 1
            market_ticket = market_models.MarketTiket.objects.create(
                market_ticket_request=market_ticket_request, ticket=ticket
            )
            market_ticket.save()
            # creating bale
            bale = market_models.Bale.objects.create(
                ticket=ticket, market_request=market_ticket_request
            )
            bale.save()

            if ticket_of == int(number_of_tickets):
                break
        create_pcn_for_additional(market_ticket_request)

        ####FOR RELEASING
        # market_ticket_request=market_models.MarketTicketRequest.objects.get(id='84ba21c1-9aa7-4b1e-ad2e-714341a661f4')
        # data1=market_models.MarketTiket.objects.filter(market_ticket_request_id=market_ticket_request.id).count()
        # data2=market_models.Bale.objects.filter(market_request_id=market_ticket_request.id).count()

        # market_models.Bale.objects.filter(market_request_id=market_ticket_request.id).delete()
        # market_models.MarketTiket.objects.filter(market_ticket_request_id=market_ticket_request.id).delete()
        # market_ticket_request.delete()
        # tkts=MarketTiket.objects.all()

        # return HttpResponse(str(data2)+' '+str(data2))
        #####END OF RELEASE

        tickets = Ticket.objects.filter(no__gte=115000)
        co = 0
        # for ti in Ticket.objects.all():
        #     ti.no =int(ti.ticket_number)
        #     ti.save()
        #     co +=1;

        # for tk in tickets:
        #     market_models.MarketTiket.objects.create(
        #             ticket_id=tk.id,
        #             market_ticket_request_id='e16d99c5-6e99-4f0c-a798-af75e073a2d8'
        #         )
        #     count +=1
        # ticket = Ticket.objects.create(
        #     print_request_id='38438944-1348-4a2a-8722-5d7761e9f0be',
        #     created_by_id=request.user.id,#User.objects.get(id=request.user.id),
        #     ticket_number=str('114999'),
        #     no=114999,
        # )
        # requid=request.GET.get('rid')

        return HttpResponse(co)

        # return render(request, template_name, {"page_obj": page_obj})
        # except:
        #   raise HttpError(500, "Internal Server Error")
    @login_required(login_url="/login")
    def add_market(request):
        try:
            form = MarketForm(request.POST or None)
            template_name = "market/add_market.html"
            if request.method == "POST":
                form = MarketForm(request.POST or None)
                if not form.is_valid():
                    print(form.errors)
                    return render(request, template_name, {"form": form})
                else:
                    if not market_table.objects.filter(market_name__iexact=request.POST.get('market_name'),region_id=request.POST.get('region')):
                        form.cleaned_data["region"] = Region.objects.filter(
                            id=request.POST.get("region")
                        ).first()
                        market = market_table.objects.create(
                            **form.cleaned_data, created_by=request.user
                        )
                        market.save()
                        messages.success(request,'Created the market '+request.POST.get('market_name'))
                        return Market.get_markets(request)
                    else:
                        messages.warning(request,'There are other market with same name in same region')

            regions = Region.objects.filter(is_active=True)
            primary_societies = Association.objects.filter(is_active=True).order_by(
                "name"
            )
            return render(
                request,
                template_name,
                {"regions": regions, "primary_societies": primary_societies},
            )
        except:
            raise HttpError(500, "Internal Server Error")

    def edit_market(request, market_id):
        try:
            form = MarketForm(request.POST or None)
            template_name = "market/add_market.html"
            if request.method == "POST":
                form = MarketForm(request.POST or None)
                if not form.is_valid():
                    print(form.errors)
                    return render(request, template_name, {"form": form})
                else:
                    form.cleaned_data["region"] = Region.objects.get(
                        id=request.POST.get("region")
                    )
                    market_table.objects.filter(id=market_id).update(
                        **form.cleaned_data
                    )
                    messages.success(request,'Updated the market')
                    return redirect("/market/market-list")
            form = market_table.objects.get(id=market_id)
            regions = Region.objects.filter(is_active=True)
            return render(
                request,
                template_name,
                {
                    "regions": regions,
                    "form": form,
                },
            )
        except :
            raise HttpError(500, "Internal Server Error")

    @login_required(login_url="/login")
    def add_print_request(request):
        data = Ticket.objects.filter(no__isnull=True)
        for dt in data:
            dt.no = dt.ticket_number
            dt.save()
        template_name = "market/add_print_request.html"
        request_form = PrintRequestForm()
        if request.method == "POST":
            form = PrintRequestForm(request.POST or None)
            if not form.is_valid():
                return render(
                    request, template_name, {"form": form, "error": form.errors}
                )
            else:
                print_request = PrintRequest.objects.create(**form.cleaned_data)
                print_request.save()
                print_request_class.genarate_request_tickets.delay(
                    request.user.id, print_request.id
                )
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Tickets Generation is on Progress, Refresh this page after 1 minutes or more to view details",
                )
            return redirect("/market/print-requests/")
        return render(request, template_name, {"form": request_form})



    @login_required(login_url="/login")

    def add_print_request_v02(request):
        """CHANGE TICKET"""
        data = Ticket.objects.filter(no__isnull=True)
        for dt in data:
            dt.no = dt.ticket_number
            dt.save()
        template_name = "market/add_print_request.html"
        form = PrintRequestForm()
        if Ticket.objects.first():
            lastticket=Ticket.objects.aggregate(no1=Max('no'))['no1']
        else:
            lastticket=None
        if request.method == "POST":
            form = PrintRequestForm(request.POST)
            last_ticket=request.POST.get('last_ticket')
            if not form.is_valid():
                return render(
                    request, template_name, {"lastticket":lastticket,"form": form, "error": form.errors}
                )
            else:
                initialticket=int(request.POST.get('initial_ticket'))
                lastticket=int(request.POST.get('last_ticket'))
                numbertickets = int(request.POST.get('number_of_tickets'))
                list1 = list(range(initialticket, lastticket))
                if not (lastticket - initialticket) == numbertickets - 1:
                    error='Range ya ticket haiko sawa hakiki tafadhali'
                    return render(request, template_name, {"form": form,'error1':error})
                if Ticket.objects.filter(no__in=list1).exists():
                    error='Range ya ticket haiko sawa hakiki, kunabaadhi ya tickets ziko kwenye range hiyo'
                    return render(request, template_name, {"form": form, 'error1': error})
                else:

                    print_request = PrintRequest.objects.create(**form.cleaned_data)
                    print_request.save()
                    print_request_class.genarate_request_tickets_v02(
                        request.user.id, print_request.id
                    )
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "Tickets Generation is on Progress, Refresh this page after 1 minutes or more to view details",
                    )
                    return redirect(reverse('market:print-requests'))
        return render(request, template_name, {"form": form,'lastticket':lastticket})

    @login_required(login_url="/login")
    def add_market_ticket_request(request):
        template_name = "market/add_market_request.html"
        market_form = MarketTicketRequestForm()
        markets = market_table.objects.filter(is_active=True)
        seasons = Season.objects.all().order_by("-id")
        primary_societies = Association.objects.filter(
                        is_active=True
                        ).order_by("name")

        staffs = Staff.objects.filter(
                        role__role_name__in=[
                            role.role_name
                            for role in Role.objects.filter(is_active=True)
                        ],
                        is_active=True,
                        ).order_by("full_name")

        if request.method == "POST":
            form = MarketTicketRequestForm(request.POST or None)
            if not form.is_valid():
                

                return render(
                        request,
                        template_name,
                        {
                            "form": form,
                            "markets": markets,
                            "primary_societies": primary_societies,
                            "staffs": staffs,
                            "message": message,
                            "seasons": seasons,
                        },
                    )
            else:
                market_tickets = list(MarketTiket.objects.values_list('ticket_id',flat=True))
                # ticket_ids = []
                # if market_tickets:
                #     ticket_ids = [ticket.ticket.id for ticket in market_tickets]
                available_tickets = Ticket.objects.filter(~Q(id__in=market_tickets)).count()

                if int(form.cleaned_data["number_of_tickets"]) <= available_tickets:
                    if MarketTicketRequest.objects.filter(ticket_request_name=form.cleaned_data["ticket_request_name"]).exists():  

                        #return redirect(request.META["HTTP_REFERER"])
                            
                        message= 'Majina ya request yanafanana'
                       
                        return render(
                            request,
                            template_name,
                            {
                                "form": form,
                                "markets": markets,
                                "primary_societies": primary_societies,
                                "staffs": staffs,
                                "message": message,
                                "seasons": seasons,
                            },
                        )
                    

                    form.cleaned_data["market"] = market_table.objects.filter(
                        market_name=form.cleaned_data["market"]
                    ).first()
                    form.cleaned_data["personnel"] = Staff.objects.filter(
                        full_name=form.cleaned_data["personnel"]
                    ).first()
                    form.cleaned_data["society"] = Association.objects.filter(
                        name=form.cleaned_data["society"]
                    ).first()
                    sales_number = 1
                    mark_request = MarketTicketRequest.objects.filter(
                        society=form.cleaned_data["society"],
                        market=form.cleaned_data["market"],
                    ).order_by("-created_on")
                    if mark_request:
                        if mark_request[0].sales_number:
                            sales_number += mark_request[0].sales_number

                    market_ticket_request = MarketTicketRequest.objects.create(
                        **form.cleaned_data,
                        created_by=request.user,
                        sales_number=sales_number,
                    )
                    market_ticket_request.ticket_request_name=market_ticket_request.ticket_request_name
                    market_ticket_request.save()

                    print_request_class.create_market_ticket(
                        request, market_ticket_request.id
                    )
                    return redirect(reverse_lazy('market:market-ticket-requests'))
                else:
                    message = f"There is no Enough Tickets in the stoke, only {available_tickets} Available"
                    primary_societies = Association.objects.filter(
                        is_active=True
                    ).order_by("name")
                    staffs = Staff.objects.filter(
                        role__role_name__in=[
                            role.role_name
                            for role in Role.objects.filter(is_active=True)
                        ],
                        is_active=True,
                    ).order_by("full_name")
                    return render(
                        request,
                        template_name,
                        {
                            "form": market_form,
                            "markets": markets,
                            "primary_societies": primary_societies,
                            "staffs": staffs,
                            "message": message,
                            "seasons": seasons,
                        },
                    )
        primary_societies = Association.objects.filter(is_active=True).order_by("name")
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ],
            is_active=True,
        ).order_by("full_name")
        return render(
            request,
            template_name,
            {
                # "form": market_form,
                "markets": markets,
                "primary_societies": primary_societies,
                "staffs": staffs,
                "seasons": seasons,
            },
        )


    def edit_market_ticket_request(request, request_id):
        template_name = "market/edit_market_request.html"
        market_form = EditMarketTicketRequestForm()
        markets = market_table.objects.filter(is_active=True)
        seasons = Season.objects.all().order_by('-id')

        if request.method == "POST":
            form = EditMarketTicketRequestForm(request.POST or None)
            data = MarketTicketRequest.objects.get(id=request_id)

            if not form.is_valid():

                return render(
                    request, template_name, {"form": form, "data": data, "message": form.errors}
                )
            else:
                #return HttpResponse(request.POST.get('society'))
                # market_tickets = MarketTiket.objects.filter(is_active=True)

                ticket_ids = []
                # if market_tickets:
                # form.cleaned_data["market"] = market_table.objects.get(
                #     id=form.cleaned_data["market"]
                # )
                form.cleaned_data["personnel"] = Staff.objects.get(
                    full_name=form.cleaned_data["personnel"]
                )
                form.cleaned_data["society"] = Association.objects.get(
                    id=request.POST.get('society')
                )
                sales_number = 1
                mark_request = MarketTicketRequest.objects.filter(
                    society=form.cleaned_data["society"],
                    market=form.cleaned_data["market"],
                ).order_by("-created_on")
                if mark_request:
                    if mark_request[0].sales_number:
                        sales_number += mark_request[0].sales_number - 1

                MarketTicketRequest.objects.filter(id=request_id).update(
                    society=form.cleaned_data["society"],
                    market_id=form.cleaned_data["market"],
                    personnel=form.cleaned_data["personnel"],
                    created_by=request.user,
                    is_mannual=form.cleaned_data["is_mannual"],
                    sales_number=form.cleaned_data["sales_number"],
                )
                return redirect("/market/market-ticket-requests")

        primary_societies = Association.objects.filter(is_active=True).order_by("name")
        staffs = Staff.objects.filter(
            role__role_name__in=[
                role.role_name for role in Role.objects.filter(is_active=True)
            ],
            is_active=True,
        ).order_by("full_name")
        form = MarketTicketRequest.objects.get(id=request_id)
        return render(
            request,
            template_name,
            {
                "form": market_form,
                "markets": markets,
                "seasons": seasons,
                "primary_societies": primary_societies,
                "staffs": staffs,
                "form": form,
            },
        )

    @login_required(login_url="/login")
    def delete_market_ticket_request(request, market_ticket_request_id):
        if not Bale.objects.filter(Q(market_request_id=market_ticket_request_id)&Q(farmer_id__isnull=False)&Q(Q(primary_weight=0)|Q(primary_weight__isnull=False))&Q(grade_id__isnull=False)).exists():
           tickst_ids=list(Bale.objects.filter(Q(market_request_id=market_ticket_request_id)).values_list('ticket_id',flat=True))
           MarketTiket.objects.filter(market_ticket_request_id=market_ticket_request_id).delete()
           Bale.objects.filter(Q(market_request_id=market_ticket_request_id)).delete()
           Ticket.objects.filter(id__in=tickst_ids).update(is_used=False)
           Pcn.objects.filter(request_id=market_ticket_request_id).delete()
           MarketTicketRequest.objects.filter(id=market_ticket_request_id).delete()
           messages.success(request,' deleted')
           return redirect(reverse('market:market-ticket-requests'))
        else:
            messages.warning(request,'Cannot delete')
            return redirect(reverse('market:market-ticket-requests'))





        

    def change_to_used(request):
        #bales=Bale.objects.all()
        count=0;
        """
        for bl in bales:
            Ticket.objects.filter(id=bl.ticket_id).update(is_used=True,no=bl.ticket.ticket_number)
            count +=1
        """
        #tickets=Ticket.objects.all()
        #return HttpResponse(MarketTiket.objects.all()[:1000].count())

        tickets=list(MarketTiket.objects.all().values_list('ticket_id',flat=True))
        Ticket.objects.filter(id__in=tickets).update(is_used=True)
        #for tk in tickets:
            #Ticket.objects.filter(id=tk.ticket_id).update(is_used=True)
            #tk.no=tk.ticket_number
            #tk.save()
            #count += 1

        return HttpResponse(MarketTiket.objects.count())
    def print_request_change(request):
        tickets=Ticket.objects.filter(no__gte=103852,no__lte=106199)
        count=m=0
        for tk in tickets:
            count +=1
            if not Bale.objects.filter(ticket_id=tk.id).exists():
                MarketTiket.objects.filter(ticket_id=tk.id).delete()
                tk.is_used=False
                tk.save()
                m +=1
        return HttpResponse(str(count)+' '+str(m))


        return redirect(reverse('market:available-tickets'))

    def change_something_old(request):
        bales = MarketWarehouseShipmentBale.objects.filter(Q(received_weight__isnull=False)&Q(Q(bale__current_weight__isnull=True)|Q(bale__current_weight=0)))

        coun=0
        #return HttpResponse(bales.count())
        for bl in bales:
            coun=coun+1
            Bale.objects.filter(id=bl.bale_id).update(
                current_grade=bl.bale.grade,current_weight=bl.received_weight,warehouse=bl.shipment.warehouse)
     
       
        return redirect(reverse('market:market-ticket-requests'))

    def sync_shipments_for_analysis(request,shipment_id):
        bales = MarketWarehouseShipmentBale.objects.filter(Q(shipment_id=shipment_id)&Q(received_weight__isnull=False)&Q(Q(bale__current_weight__isnull=True)|Q(bale__current_weight=0)))

        coun=0
        #return HttpResponse(bales.count())
        for bl in bales:
            coun=coun+1
            Bale.objects.filter(id=bl.bale_id).update(
                current_grade=bl.bale.grade,current_weight=bl.received_weight,warehouse=bl.shipment.warehouse)
     
       
        return redirect(reverse('shipment:market-warehouse-details',kwargs={'shipment_id':shipment_id}))


    def old_pcn_verify(request):
        bales = Pcn.objects.update(is_data_verified=True)
        return HttpResponse(Pcn.objects.count())
    # def old_problem_128522(request):
    #     tik=Ticket.objects.filter(no='128522').first()
    #     MarketTiket.objects.create(ticket_id=tik.id,market_ticket_request_id='2d38ab44-ccdd-47c2-a83e-b650f2f9e135')
    #     Bale.objects.create(ticket_id=tik.id,market_request_id='2d38ab44-ccdd-47c2-a83e-b650f2f9e135',pcn_id='d14820b9-183c-40b7-8e7f-f7f56d3a63c5')
    #     return redirect(reverse('pcn-detail',kwargs={'pcn_id':'d14820b9-183c-40b7-8e7f-f7f56d3a63c5'}))

    def calculate_verified_value(request):
        bales=Bale.objects.filter(verified_grade_id__isnull=False,verifiedvalue__isnull=True).order_by('created_on')
        count=0
        for bale in bales:
            priceobj = GradePrice.objects.filter(
                grade_id=bale.verified_grade_id
                ).first()
            if priceobj:
               
                bale.verifiedvalue= round(priceobj.price * float(bale.primary_weight), 2)
                count =count+1
            else:
                bale.verifiedvalue = 0
            bale.save()
        return HttpResponse(count)

        """
        if edit_bale_schema["grade"] and edit_bale_schema["primary_weight"]:
            weight = edit_bale_schema["primary_weight"]
            if not weight or weight == "":
                weight = "0"
            priceobj = GradePrice.objects.filter(
                grade_id=edit_bale_schema["grade"]
            ).first()
            if priceobj:
                edit_bale_schema["price"] = priceobj.price
                edit_bale_schema["value"] = round(priceobj.price * float(weight), 2)
            else:
                edit_bale_schema["value"] = 0
        """
        
    def test_email(request): 
        from django.core.mail import EmailMessage, get_connection
        from django.conf import settings
        frp=None
        #if request.method == "POST":
        emails=list(SendingShipmentEmail.objects.values_list('email',flat=True))
        with get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD, use_tls=settings.EMAIL_USE_TLS  ) as connection:  
           subject = 'SUB'  
           email_from = settings.EMAIL_HOST_USER  
           recipient_list = emails 
           message = 'Dear Team \n'
           message +=' Attached shippment number '+str(36474)+' On any case please reply to this email'
           message +='\n Best Regards '
           message +='\n Capture Software'
           reply_to=['esterghuliku@gmail.com','kyomo89elieza@gmail.com']
           headers={'Message-ID': str(2345)},
           email=EmailMessage(subject, message, email_from, recipient_list,reply_to=reply_to, connection=connection)
           email.attach_file(os.path.join(settings.MEDIA_ROOT, 'shipment/CSV-AUG-01.csv'))
           email.send()
        return HttpResponse(frp)

 
        """
        from django.core.mail import send_mail
        from django.conf import settings
        subject = 'Thank you for registering to our site'
        message = ' it  means a world to us '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['kyomo89elieza@gmail.com','eliezer.kyomo@mifumotz.com']
        data=send_mail(subject, message, email_from, recipient_list,fail_silently = False )
        return HttpResponse(data)
        """



        #reqob=market_models.MarketTicketRequest.objects.filter(is_mannual=True,created_on__gte='2023-03-07').latest('created_on')
        #req_id=reqob.id#'b919a359-c24e-407d-8f10-cfffa358d91b'
        #printreqOB=market_models.PrintRequest.objects.filter(is_mannual=True,created_on__gte='2023-03-07').latest('created_on')

        #return HttpResponse(str(reqob.sales_date)+'  '+str(printreqOB.initial_ticket))

    @login_required(login_url="/login")
    def get_available_tickets(request):
        #try:
        template_name = "market/tickets/available_tickets.html"
        print_request_tickets = Ticket.objects.values(rname=F('print_request__request_name'),rid=F('print_request_id'),is_mannual1=F('print_request__is_mannual')).annotate(
            total=Count('id'),
            mint=Min('no'),
            maxt=Max('no'),
            used=Sum(Case(When(is_used=True, then=Value(1)),),default=Value(0),output_field=IntegerField()),
            available=Sum(Case(When(is_used=False, then=Value(1)), ), default=Value(0), output_field=IntegerField()),
        ).order_by('-print_request__created_on')

        return render(request, template_name, {"boxes": print_request_tickets})
        #except:
        #    raise HttpError(500, "Internal Server Error")

    @login_required(login_url="/login")
    def get_used_tickets(request):
        try:
            template_name = "market/tickets/used_tickets.html"
            used_tickets = MarketTiket.objects.raw(
                """select mkt.market_name, mkt.id, count(mtkt.ticket_id) as used_tickets,
                    (select tkt.ticket_number from public.ticket tkt, public.market_ticket mt, public.market_ticket_request mtr where mtr.id=mt.market_ticket_request_id and  tkt.id=mt.ticket_id and mtr.market_id=mkt.id  group by tkt.ticket_number  order by tkt.ticket_number ASC LIMIT 1) as ticket_number_start,
					(select tkt.ticket_number from public.ticket tkt, public.market_ticket mt, public.market_ticket_request mtr where mtr.id=mt.market_ticket_request_id and  tkt.id=mt.ticket_id and mtr.market_id=mkt.id  group by tkt.ticket_number  order by tkt.ticket_number DESC LIMIT 1 ) as ticket_number_end
                     from public.market mkt, public.market_ticket_request mtktr, public.market_ticket mtkt, public.ticket tk where mtkt.ticket_id = tk.id and mtktr.id = mtkt.market_ticket_request_id and mkt.id = mtktr.market_id and tk.id in (select ticket_id from public.market_ticket) group by mkt.market_name, mkt.id"""
            )
            paginated_print_request_tickets = Paginator(used_tickets, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_print_request_tickets.get_page(page_number)
            return render(request, template_name, {"page_obj": page_obj})

        except:
            raise HttpError(500, "Internal Server Error")

    @login_required(login_url="/login")
    def assign_personnel(request):
        try:
            template_name = "market/add_market_personnel.html"
            if request.method == "POST":
                market_personnel_form = MarketTicketRequestPersonnelForm(
                    request.POST, None
                )
                if market_personnel_form.is_valid():
                    market_ticket_request = market_models.Market.objects.get(
                        ticket_request_name=market_personnel_form.cleaned_data[
                            "request_name"
                        ]
                    )
                    personnel = Staff.objects.get(
                        full_name=market_personnel_form.cleaned_data["personnel"]
                    )
                    market_personnel = (
                        market_models.MarketTicketRequestPersonnel.objects.create(
                            market_ticket_request=market_ticket_request,
                            personnel=personnel,
                        )
                    )
                    market_personnel.save()
                    return Market.market_assignments(request)
            markets = market_models.Market.objects.filter(is_active=True).order_by(
                "market_name"
            )
            personnels = Staff.objects.filter(is_active=True).order_by("full_name")
            return render(
                request, template_name, {"markets": markets, "personnels": personnels}
            )
        except:
            raise HttpError(500, "Internal Server Error")

    @login_required(login_url="/login")
    def market_assignments(request):
        try:
            template_name = "market/market_assignments.html"
            market_personnels = MarketTicketRequestPersonnel.objects.filter(
                is_active=True
            ).order_by("-created_on")
            paginated_market_personnels = Paginator(market_personnels, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_market_personnels.get_page(page_number)
            return render(request, template_name, {"page_obj": page_obj})
        except:
            raise HttpError(500, "internal Server Error")

    @login_required(login_url="/login")
    def release_ticket_from_request(request, request_id):
        data = Ticket.objects.filter(no__isnull=True)
        for dt in data:
            dt.no = dt.ticket_number
            dt.save()
        """Release Unused tickets"""
        template_name = "market/pcn/relese_ticket.html"
        market_request=MarketTicketRequest.objects.get(id=request_id)
        form = TicketReleaseForm()
        if request.method == "POST":
            form = MarketTicketRequestForm(request.POST or None)
            if not form.is_valid():
                return render(
                    request, template_name, {"form": form, "message": form.errors,'market_request':market_request}
                )
            else:
                first = int(request.POST.get("first"))
                last = int(request.POST.get("last"))
                ##CHECK IF ALL THE BALES IN THIS RANGE HAVE NO DATA
                #return HttpResponse(first)
                if not Bale.objects.filter(
                    Q(ticket__no__gte=first)
                    & Q(ticket__no__lte=last)
                    & Q(market_request_id=request_id)
                    & Q(primary_weight__isnull=False )
                ).exists():

                    bales_ids = list(
                        Bale.objects.filter(
                            Q(ticket__no__gte=first)
                            & Q(ticket__no__lte=last)
                            & Q(market_request_id=request_id)
                        ).values_list("ticket_id", flat=True)
                    )
                    # RElease from MarketTicket
                    MarketTiket.objects.filter(ticket_id__in=bales_ids).delete()
                    # Release from Balase
                    Bale.objects.filter(ticket_id__in=bales_ids).delete()
                    # need to be reviewed
                    Ticket.objects.filter(id__in=bales_ids).update(is_used=False)
                    messages.success(
                        request,
                        "Successfull release from " + str(first) + " to " + str(last),
                    )
                    return redirect(
                        reverse("market:request-details", kwargs={"request_id": request_id})
                    )
                else:
                     return render(request, template_name, {"form": form,'market_request':market_request,'error':'Angalia vema baadhi zina data'})


        else:
            return render(request, template_name, {"form": form,'market_request':market_request})


    @login_required(login_url="/login")
    def aditional_ticket_from_request(request, request_id):
        data = Ticket.objects.filter(no__isnull=True)
        for dt in data:
            dt.no = dt.ticket_number
            dt.save()
        """Release Unused tickets"""
        template_name = "market/pcn/additional_ticket.html"
        market_request=MarketTicketRequest.objects.get(id=request_id)
        form = AdditionalTicketForm()
        if request.method == "POST":
            form = MarketTicketRequestForm(request.POST or None)
            if not form.is_valid():
                return render(
                    request, template_name, {"form": form, "message": form.errors,'market_request':market_request}
                )
            else:
                lists = list(market_models.MarketTiket.objects.values_list('ticket_id', flat=True))
                tickets = Ticket.objects.filter(~Q(id__in=lists)&Q(is_used=False)&Q(created_on__gte='2023-02-01')).order_by('no')
                no_tickets = int(request.POST.get("no_tickets"))
                market_tickets = list(MarketTiket.objects.values_list('ticket_id',flat=True))
                # ticket_ids = []
                # if market_tickets:
                #     ticket_ids = [ticket.ticket.id for ticket in market_tickets]
                available_tickets = Ticket.objects.filter(~Q(id__in=market_tickets)&Q(is_used=False)&Q(created_on__gte='2023-02-01')).count()

                #available_tickets = Ticket.objects.exclude(id__in=ticket_ids).count()
                ##CHECK IF ALL THE BALES IN THIS RANGE HAVE NO DATA
                #return HttpResponse(first)
                if int(no_tickets) <= available_tickets:

                    number_of_tickets = no_tickets
                    ticket_of = 0
                    dbale=[]
                    markettdb=[]
                    for ticket in tickets:
                        ticket_of += 1
                        markettdb.append(market_models.MarketTiket(
                            market_ticket_request_id=market_request.id, ticket_id=ticket.id
                        ))
                        #market_ticket.save()
                        # creating bale
                        dbale.append(market_models.Bale(
                            ticket_id=ticket.id, market_request_id=market_request.id
                        ))
                        ticket.is_used=True
                        ticket.save()

                        if ticket_of == int(number_of_tickets):
                            break
                    market_models.Bale.objects.bulk_create(dbale)
                    market_models.MarketTiket.objects.bulk_create(markettdb)
                    create_pcn_for_additional(market_request)

                    
                    messages.success(
                        request,
                        "Successfull added tickets from " + str(no_tickets) 
                    )
                    return redirect(
                        reverse("market:request-details", kwargs={"request_id": request_id})
                    )
                else:
                     return render(request, template_name, {"form": form,'market_request':market_request,'error':'Quantity available is less than required'})


        else:
            return render(request, template_name, {"form": form,'market_request':market_request})



class Buyer:
    @login_required(login_url="/login")
    def add_buyer(request):
        template_name = "market/add_buyer.html"
        if request.method == "POST":
            form = BuyerForm(request.POST or None)
            if form.is_valid():
                buyer = market_models.Buyer.objects.create(**form.cleaned_data)
                buyer.save()
                return redirect("/market/buyers")
        return render(request, template_name)

    


    def edit_buyer(request, buyer_id):
        template_name = "market/add_buyer.html"
        if request.method == "POST":
            form = BuyerForm(request.POST or None)
            if form.is_valid():
                market_models.Buyer.objects.filter(id=buyer_id).update(
                    **form.cleaned_data
                )
                return redirect("/market/buyers")
        form = market_models.Buyer.objects.get(id=buyer_id)
        return render(request, template_name, {"form": form})

    @login_required(login_url="/login")
    def get_buyers(request):
        status=request.GET.get('status')
        #return HttpResponse(status))
        is_Active=True
        header = ' Buyers'
        if status:
            if int(status) == 0:
                is_Active=False
                header='Inactive Buyers'


        template_name = "market/buyers.html"
        buyers = market_models.Buyer.objects.filter(is_active=is_Active).order_by(
            "buyer_code"
        )
        paginated_buyers = Paginator(buyers, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_buyers.get_page(page_number)
        return render(request, template_name, {"page_obj": buyers,'header':header})

    @login_required(login_url="/login")
    def delete_buyer(request, buyer_id):
        buyer = market_models.Buyer.objects.get(id=buyer_id)
        if buyer.is_active:
            buyer.is_active=False
            messages.success(request,'Deactivated buyer')
        else:
            buyer.is_active=True
            messages.success(request, 'Activated buyer')
        buyer.save()
        return redirect("/market/buyers")


###PCN FUNCTION
class PCN:
    @login_required(login_url="/login")
    def get_pcn_detail(request, pcn_id):
        """GET PCN DETAIL USING PCN_ID"""
        template_name = "market/pcn/pcn_details.html"
        # try:
        context = {}
        context["pcn"] = pcn = Pcn.objects.get(id=pcn_id)
        context["market_request"] = pcn.request
        context["bales"] = Bale.objects.filter(pcn_id=pcn.id).order_by("created_on")
        context["pcn_total"] = (
            Bale.objects.filter(pcn_id=pcn_id)
            .values(nll=F("pcn__nill"))
            .annotate(
                valueT=Sum("value"),
                primary_weightT=Sum("primary_weight"),
                noTotal=Count("id"),
            )
        )

        return render(request, template_name, context)
        # except:
        raise HttpError(500, "Internal Server Error")

    @login_required(login_url="/login")
    def unlink_tickets_from_pcn(request, pcn_id):
        """UNLINK TICKETS FROM PCN"""
        pcnOB=Pcn.objects.get(id=pcn_id)
        Bale.objects.filter(pcn_id=pcn_id).update(pcn_id='')
        #return redirect(reverse('market:request-details',pcnOB.request_id))
        return redirect(reverse('market:request-details',kwargs={'request_id':pcnOB.request_id})) 
        
    @login_required(login_url="/login")
    def refresh_pcn_and_tickets(request, request_id):
        """REFRESH PCN ON TICKETS"""
        reqob=MarketTicketRequest.objects.get(id=request_id)
        create_pcn_for_additional(reqob)
        return redirect(reverse('market:request-details',kwargs={'request_id':request_id})) 

    @login_required(login_url="/login")
    def get_pcn_detail_for_update(request, pcn_id):
        """GET PCN DETAIL USING PCN_ID"""
        template_name = "market/pcn/pcn_update.html"
        # try:
        context = {}
        context["pcn"] = pcn = Pcn.objects.get(id=pcn_id)
        context["buyers"] = Buyer_table.objects.filter(is_active=True)
        context["market_request"] = pcn.request
        context["bales"] = Bale.objects.filter(pcn_id=pcn.id).order_by("created_on")
        return render(request, template_name, context)
        # except:
        raise HttpError(500, "Internal Server Error")

    @login_required(login_url="/login")
    def single_bale_update(request, request_id):
        season_id = request.GET.get("season_id")
        bale_id = request.GET.get("ticket_id")
        price = request.GET.get("price").replace("$", "")
        if "" in price:
            price = "0"
        # price = request.GET.get('price').replace('$', '')
        weight = float(request.GET.get("weight"))
        if not weight or weight == "":
            weight = "0"
        tweight = request.GET.get("tweight")
        value = request.GET.get("value")
        value = value.replace("$", "")

        status = request.GET.get("remarks")
        price = float(request.GET.get("price").replace("$", ""))
        price = request.GET.get("price").replace("$", "")
        grade = request.GET.get("grade")
        buyer_code = request.GET.get("buyer_code")
        gradeob = CropGrade.objects.filter(grade_name__iexact=grade).first()
        # value=request.GET.get('value').replace('$','')
        priceobj = GradePrice.objects.filter(
            grade__grade_name__iexact=grade, season_id=season_id
        ).first()
        if priceobj:
            value = round(priceobj.price * float(weight), 2)
        else:
            value = 0
        tik = Bale.objects.filter(id=bale_id, market_request_id=request_id)
        # return HttpResponse(priceobj.price)
        if gradeob:
            if (status).upper() == "R":
                tik.update(
                    buyer_code=buyer_code,
                    grade_id=gradeob.id,
                    primary_weight=weight,
                    price=price,
                    value=value,
                    status=status,
                )

            elif (status).upper() == "W":
                tik.update(
                    buyer_code=buyer_code,
                    grade_id=gradeob.id,
                    primary_weight=weight,
                    price=price,
                    value=value,
                    status=status,
                )
            else:
                tik.update(
                    buyer_code=buyer_code,
                    grade_id=gradeob.id,
                    primary_weight=weight,
                    price=price,
                    value=value,
                    status=status,
                )
            if tweight != "":
                MarketWarehouseShipmentBale.objects.filter(bale_id=bale_id).update(
                    transport_weight=tweight
                )

        return HttpResponse(value)  # tik.first().ticket.ticket_no)

    @login_required(login_url="/login")
    def get_grade_price(request, season_id):
        name = request.GET.get("name")
        season = season_id
        if name:
            if season:
                sale = GradePrice.objects.filter(
                    grade__grade_name__iexact=name,
                    season_id=season,
                    grade__is_active=True,
                )
                if sale:
                    return HttpResponse(str(sale.first().price))
                else:
                    return HttpResponse("")

            else:
                last = Season.objects.all().last()
                sale = GradePrice.objects.filter(
                    grade__grade_name__iexact=name,
                    season_id=last.id,
                    grade__is_active=True,
                ).order_by("-created_on")
                if sale:
                    return HttpResponse(str(sale.first().price))
                else:
                    return HttpResponse("")

        else:
            return HttpResponse("")

    @login_required(login_url="/login")
    def get_buyers(request):
        template_name = "market/buyers.html"
        buyers = market_models.Buyer.objects.all().order_by("full_name")
        paginated_buyers = Paginator(buyers, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_buyers.get_page(page_number)
        return render(request, template_name, {"page_obj": page_obj})

    @login_required(login_url="/login")
    def verify_pcn(request, pcn_id):
        Pcn.objects.filter(id=pcn_id).update(
            is_data_verified=True, data_verification_by=request.user
        )
        messages.success(request, "Successful VERIFIED")
        return redirect(reverse("market:pcn-detail", kwargs={"pcn_id": pcn_id}))

    @login_required(login_url="/login")
    def deverify_pcn(request, pcn_id):
        Pcn.objects.filter(id=pcn_id).update(
            is_data_verified=False, data_verification_by=None
        )
        messages.success(request, "Successful DISVERIFIED")
        return redirect(reverse("market:pcn-detail", kwargs={"pcn_id": pcn_id}))

    @login_required(login_url="/login")
    def pcn_single_pdf(request, pcn_id):
        template_name = "market/pcn/pdf/pdf_empty_pcn_single.html"
        template_name_data = "market/pcn/pdf/pdf_data_pcn_single.html"
        type = request.GET.get("type")
        pcn = Pcn.objects.get(id=pcn_id)
        saleno = pcn.request.sales_number
        market_id = pcn.request.market_id
        society_id = pcn.request.society_id
        context = {}
        context["market"] = req = pcn.request
        context["pcn"] = pcn
        context["date"] = datetime.today()
        context["bales"] = Bale.objects.filter(pcn_id=pcn_id).order_by("created_on")
        context["pcns"] = (
            Bale.objects.filter(pcn_id=pcn_id)
            .values(
                pcnn=F("pcn__pcn_no"),
                mcenter=F("pcn__request__market__market_name"),
                saleno=F("pcn__request__sales_number"),
                saledate=F("pcn__request__sales_date"),
            )
            .annotate(
                total=Count("id"),
                init=Min("ticket__ticket_number"),
                last=Max("ticket__ticket_number"),
            )
        )
        if type:
            context["ticketstota"] = (
                Bale.objects.filter(Q(pcn_id=pcn_id) & ~Q(status="R") & ~Q(status="W"))
                .values(
                    pcnn=F("pcn__pcn_no"),
                    pcn_nid=F("pcn_id"),
                    mname=F("pcn__request__market__market_name"),
                    societyname=F("pcn__request__society__name"),
                )
                .annotate(
                    count=Count("id"),
                    weight_t=Sum("primary_weight"),
                    value_t=Sum("value"),
                )
            )
            pdf = common_render_to_pdf(template_name_data, context, "file")
            fname = pcn.pcn_no + "-DATA"
        else:
            pdf = common_render_to_pdf(template_name, context, "file")
            fname = pcn.pcn_no + "-EMPTY"

        if pdf:
            response = HttpResponse(pdf, content_type="application/force-download")
            content = "attachment; filename=%s.pdf  " % fname
            response["Content-Disposition"] = content
            return response
        else:
            return HttpResponse("Not found")

    @login_required(login_url="/login")
    def pcn_all_pdf(request, request_id):
        template_name = "market/pcn/pdf/empty_all_pcn_pdf.html"
        template_name_data = "market/pcn/pdf/all_data_pcn.html"
        type = request.GET.get("type")

        context = {}
        context["pcns"] = Pcn.objects.filter(request_id=request_id).order_by("no")
        context[
            "requestOB"
        ] = requestOB = market_models.MarketTicketRequest.objects.get(id=request_id)
        context["market"] = req = requestOB
        fname = (
            requestOB.market.market_name
            + " "
            + requestOB.society.name
            + " SALENO-"
            + str(requestOB.sales_number)
            + ""
        )
        if type:
            pdf = common_render_to_pdf(template_name_data, context, "file")
            fname = "DATA-" + fname
        else:
            pdf = common_render_to_pdf(template_name, context, "file")
            fname = "EMPTY-" + fname

        if pdf:
            response = HttpResponse(pdf, content_type="application/force-download")
            content = "attachment; filename=%s.pdf  " % fname
            response["Content-Disposition"] = content
            return response
        else:
            return HttpResponse("Not found")


class Verifier:
    def add_verifier(request):
        template_name = "market/verifier/add.html"
        header='Add Verifier'
        if request.method == "POST":
            form = VerifyForm(request.POST or None)
            if form.is_valid():
                if not market_models.GradeVerifier.objects.filter(code=request.POST.get('code')).exists():

                    buyer = market_models.GradeVerifier.objects.create(**form.cleaned_data)
                    buyer.save()
                    messages.success(request, 'Verifier successfully created')
                messages.warning(request,'Verifier Code Exist')
                return redirect(reverse('market:verifiers'))
        return render(request, template_name,{'header':header})

    


    def edit_verifier(request, verifier_id):
        template_name = "market/verifier/edit.html"
        if request.method == "POST":
            form = VerifyForm(request.POST or None)
            if form.is_valid():
                market_models.GradeVerifier.objects.filter(id=verifier_id).update(
                    **form.cleaned_data
                )
                return redirect(reverse('market:verifiers'))
        form = market_models.GradeVerifier.objects.get(id=verifier_id)
        return render(request, template_name, {"form": form})

    def refresh_prices_on_2023(request, request_id):
        ReqOB=market_models.MarketTicketRequest.objects.filter(id=request_id).first()
        bales =market_models.Bale.objects.filter(market_request_id=request_id)
        for bl in bales:
            priceobj=GradePrice.objects.filter(
                grade_id=bl.grade_id,
                season_id=ReqOB.season_id
            ).latest('created_on')
            if priceobj:
                bl.price = priceobj.price
                bl.value = round(priceobj.price * float(bl.primary_weight), 2)
            else:
                edit_bale_schema["value"] = 0
            bl.save()

        return redirect(reverse('market:request-detail-tickets',kwargs={'request_id':request_id}))


    @login_required(login_url="/login")
    def get_verifiers(request):
        template_name = "market/verifier/verifiers.html"
        STAT=request.POST.get('status')
        header = ' Verifiers'
        isACtive=True
        if STAT:
            if int(STAT) == 0:
                isACtive=False
                header='Inactive Verifiers'

        buyers = market_models.GradeVerifier.objects.filter(is_active=isACtive).order_by(
            "full_name"
        )
        return render(request, template_name, {"buyers": buyers,'header':header})

    @login_required(login_url="/login")
    def delete_verifier(request, verifier_id):
        buyer = market_models.GradeVerifier.objects.get(id=verifier_id)
        if buyer.is_active:
            buyer.is_active=False
            messages.success(request,'Buyer deactivated')
        else:
            buyer.is_active = True
            messages.success(request, 'Buyer activated')

        return redirect(reverse('market:verifiers'))


class BaleView:
    @login_required(login_url="/login")
    def get_bale_info(request):
        context={}
        template_name = "bale/bale_info.html"
        context['ticket']=ticket=request.GET.get('ticket_number')
        context['header']='BALE INFORMATION'
        context['ticket'] = market_models.Ticket.objects.filter(ticket_number=ticket).first()
        context['bale']  = line = market_models.Bale.objects.filter(ticket__ticket_number=ticket).first()
        context['line']=line
        context['form']=BaleForm
        context['gshipmentinfo'] =GeneralShipmentBale.objects.filter(bale__ticket__ticket_number=ticket).first()
        context['mshipmentinfo'] =MarketWarehouseShipmentBale.objects.filter(bale__ticket__ticket_number=ticket).first()
        return render(request, template_name, context)

    @login_required(login_url="/login")
    def beyond_the_weight(request):
        context={}
        context['bales']=market_models.Bale.objects.filter(primary_weight__gt=90).order_by('ticket__ticket_number')
        context['mshipment']=MarketWarehouseShipmentBale.objects.filter(Q(transport_weight__gt=90)|Q(received_weight__gt=90)).order_by('bale__ticket__ticket_number')
        context['gshipment']=GeneralShipmentBale.objects.filter(Q(transport_weight__gt=90)).order_by('bale__ticket__ticket_number')
        return render(request,'bale/excess_weight.html',context)

    @login_required(login_url="/login")
    def edit_bale(request, bale_id):
        form = BaleEditForm()
        template_name = "bale/edit_bale.html"
        if request.method == "POST":
            form = BaleEditForm(request.POST or None)
            weight=request.POST.get('primary_weight')

            if form.is_valid():
                market_models.Bale.objects.filter(id=bale_id).update(
                    **form.cleaned_data
                )
                bale=market_models.Bale.objects.filter(id=bale_id).first()

                priceobjF = GradePrice.objects.filter(
                grade_id=bale.grade_id
                ).first()

                priceobj = GradePrice.objects.filter(
                grade_id=bale.verified_grade_id
                ).first()
                if priceobj:
                   
                    bale.verifiedvalue= round(priceobj.price * float(bale.primary_weight), 2)
                   
                else:
                    bale.verifiedvalue = 0
                if priceobjF:
                    bale.value= round(priceobjF.price * float(bale.primary_weight), 2)
                   
                else:
                    bale.value = 0

                bale.save()
                return redirect(reverse('market:beyond_the_weight'))
        bale = market_models.Bale.objects.get(id=bale_id)
        return render(request, template_name, {"form": form,'bale':bale})

    @login_required(login_url="/login")
    def edit_marketShipment_bale(request, trans_id):
        form = BaleEditMarketWarehouse()
        template_name = "bale/edit_bale_market_shipment.html"
        if request.method == "POST":
            form = BaleEditMarketWarehouse(request.POST or None)
            received_weight=request.POST.get('received_weight')

            if form.is_valid():
                MarketWarehouseShipmentBale.objects.filter(id=trans_id).update(
                    **form.cleaned_data
                )
                bale=MarketWarehouseShipmentBale.objects.filter(id=trans_id).first().bale
                bale.current_weight=received_weight

                bale.save()
                return redirect(reverse('market:beyond_the_weight'))
        bale = MarketWarehouseShipmentBale.objects.get(id=trans_id)
        return render(request, template_name, {"form": form,'trans':bale})

    @login_required(login_url="/login")
    def edit_GeneralShipment_bale(request, transb_id):
        form = BaleEditGeneralShipmentWarehouse()
        template_name = "bale/edit_bale_market_shipment.html"
        if request.method == "POST":
            form = BaleEditGeneralShipmentWarehouse(request.POST or None)
            received_weight=request.POST.get('received_weight')

            if form.is_valid():
                GeneralShipmentBale.objects.filter(id=transb_id).update(
                    **form.cleaned_data
                )
               
                return redirect(reverse('market:beyond_the_weight'))
        bale = GeneralShipmentBale.objects.get(id=transb_id)
        return render(request, template_name, {"form": form,'trans':bale})


class UpdateSaveMannualTicketView(CreateView):

    login_url ="/login"
    redirect_field_name = 'next'
    form_class=UpdateTicketUsingTicketNoForm
    template_name='bale/mannual/add_update.html'
    context_object_name='form'
    success_url=reverse_lazy('market:mannual_verify')


    def post(self,request,*args,**kwargs):

        form=self.form_class(request.POST)
        if form.is_valid():

            """"""
            req_id='b919a359-c24e-407d-8f10-cfffa358d91b'
            print_request_id='c0b4859e-80c7-4fcf-8447-67709975d024'
           
            
            #####################################
            ##GRADE PRICES
            ##################################
            
            grade=request.POST.get('grade')
            primary_weight=request.POST.get('primary_weight')
            current_weight=request.POST.get('current_weight')
            ticket_number=request.POST.get('ticket_number')
            verifier=request.POST.get('verifier')
            verified_grade=request.POST.get('verified_grade')
            in_house_grade=request.POST.get('in_house_grade')
            buyer=request.POST.get('buyer')
            buyer_code=market_models.Buyer.objects.get(id=buyer).buyer_code
            warehouse=request.POST.get('warehouse')

            mn_society=request.POST.get('society')
            mn_market=request.POST.get('market')

            
            verivalue=value=0
            if grade and primary_weight:
                weight = primary_weight
                if not weight or weight == "":
                    weight = "0"
                priceobj = GradePrice.objects.filter(
                    grade_id=grade
                ).first()
                if priceobj:
                    price = priceobj.price
                    value = round(priceobj.price * float(weight), 2)
                else:
                    value = 0
            if verified_grade and current_weight:
                weight = current_weight
                if not weight or weight == "":
                    weight = "0"
                priceobj = GradePrice.objects.filter(
                    grade_id=verified_grade
                ).first()
                if priceobj:
                    price = priceobj.price
                    verivalue = round(priceobj.price * float(weight), 2)
                else:
                    verivalue = 0

            ###END PRICES
            #####################################

            if market_models.Bale.objects.filter(market_request_id=req_id,ticket__ticket_number=ticket_number).exists():
                bale = market_models.Bale.objects.filter(market_request_id=req_id,ticket__ticket_number=ticket_number).update(
                    current_grade_id=verified_grade,
                    grade_id=grade,
                    current_weight=current_weight,
                    primary_weight=primary_weight,
                    warehouse_id=warehouse,
                    verified_grade_id=verified_grade,
                    in_house_grade_id=in_house_grade,
                    verifier_id=verifier,
                    verifiedvalue=verivalue,
                    value=value,
                    buyer_code=buyer_code,
                    is_mannual=True,
                    mn_society_id=request.POST.get('society'),
                    mn_market_id=request.POST.get('market'),
                    verification_date=datetime.now()
                )
                bale = market_models.Bale.objects.filter(market_request_id=req_id,ticket__ticket_number=ticket_number)
                #return HttpResponse(ticket_number'])

            else:
                if not  market_models.Ticket.objects.filter(ticket_number=str(ticket_number)).exists():

                    ticket = market_models.Ticket.objects.create(
                        print_request_id=print_request_id,
                        created_by=User.objects.all().first(),#(id=user_data.id),
                        ticket_number=str(ticket_number),
                        no=int(ticket_number)
                        )
                    market_ticket = market_models.MarketTiket.objects.create(market_ticket_request_id=req_id, ticket_id=ticket.id)
                    market_ticket.save()
                    # creating bale
                    bale = market_models.Bale.objects.create(
                        ticket_id=ticket.id,
                        market_request_id=req_id,
                        current_grade_id=verified_grade,
                        grade_id=grade,
                        current_weight=current_weight,
                        primary_weight=primary_weight,
                        warehouse_id=warehouse,
                        verified_grade_id=verified_grade,
                        in_house_grade_id=in_house_grade,
                        verifier_id=verifier,
                        buyer_code=buyer_code,
                        verifiedvalue=verivalue,
                        value=value,
                        is_mannual=True,
                        mn_society_id=request.POST.get('society'),
                        mn_market_id=request.POST.get('market'),
                       
                        verification_date=datetime.now()
                    )
                    if bale:
                        ticket.is_used=True
                        ticket.save()
                    bale = market_models.Bale.objects.filter(market_request_id=req_id,ticket__ticket_number=ticket_number)
                else:
                    if not market_models.Bale.objects.filter(ticket__ticket_number=ticket_number).exists(): 

                        ticket=market_models.Ticket.objects.filter(ticket_number=str(ticket_number)).first()
                        
                        market_ticket = market_models.MarketTiket.objects.update_or_create(market_ticket_request_id=req_id, ticket_id=ticket.id)

                        

                        
                        # creating bale
                        bale,created = market_models.Bale.objects.update_or_create(
                            ticket_id=ticket.id,
                            market_request_id=req_id,
                            current_grade_id=verified_grade,
                            grade_id=grade,
                            current_weight=current_weight,
                            primary_weight=primary_weight,
                            warehouse_id=warehouse,
                            verified_grade_id=verified_grade,
                            in_house_grade_id=in_house_grade,
                            verifier_id=verifier,
                            buyer_code=buyer_code,
                            verifiedvalue=verivalue,
                            value=value,
                            is_mannual=True,
                            mn_society_id=request.POST.get('society'),
                            mn_market_id=request.POST.get('market'),
                            verification_date=datetime.now())
                        bale = market_models.Bale.objects.filter(market_request_id=req_id,ticket__ticket_number=ticket_number)
                        if bale:
                            ticket.is_used=True
                    else:
                        bale=None
            if bale:
                messages.success(request,'Saved successfull')
                return redirect(self.success_url)
            else:
                return render(self.request,self.template_name,{'form':form})


        return render(self.request,self.template_name,{'form':form})  


class LatestBales(ListView):
    login_url = "/login"
    redirect_field_name = 'next'
    model=Bale
    template_name='bale/mannual/bales.html'
    context_object_name='bales'
    order_by=['-id']
    
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data()
        return context     






