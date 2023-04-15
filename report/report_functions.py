from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from xhtml2pdf import pisa
from django.db.models import (
    FloatField,
    F,
    Sum,
    Max,
    Case,
    When,
    IntegerField,
    Value,
    Min,
    Q,
    Count,
)
from .models import *
from .forms import *
from market.models import Bale, MarketTicketRequest, Pcn
from shipment.models import GeneralShipmentBale

############################SOCIETIES SALES REPORT
def allsociety_pcn_total_yearly(year):
    return (
        Bale.objects.filter(pcn__request__season_id=year, pcn__is_data_verified=True,primary_weight__isnull=False)
        .values("pcn__nill")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            salenos=Count("pcn__request_id", distinct=True),
        )
    )


def allsociety_pcn_listsum_yearly(year):
    return (
        Bale.objects.filter(pcn__request__season_id=year, pcn__is_data_verified=True,primary_weight__isnull=False,pcn__request__on_pre_buying=False,pcn__request__on_buying=False)
        .values(psociety=F("pcn__request__society__name"))
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            salenos=Count("pcn__request_id", distinct=True),
        )
        .order_by('psociety')
    )


#################################################

########


def single_society_sale_total(society, year):
    return (
        Bale.objects.filter(
            pcn__request__society_id=society,
            pcn__request__season_id=year,
            pcn__is_data_verified=True,
            primary_weight__isnull=False
        )
        .values("pcn__nill")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )


def single_society_sale_list(society, year):
    return (
        Bale.objects.filter(
            pcn__request__society_id=society,
            pcn__request__season_id=year,
            pcn__is_data_verified=True,
            primary_weight__isnull=False
        )
        .values(
            mcenter=F("pcn__request__market__market_name"),
            saleno=F("pcn__request__sales_number"),
            saledate=F("pcn__request__sales_date"),
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('pcn__no')
    )


######################################################
##########REGIONAL PAID DATA
def reional_society_paid_list(region, year):
    return (
        Bale.objects.filter(
            pcn__request__society__region_id=region,
            pcn__request__season_id=year,
            pcn__is_data_verified=True,
            primary_weight__isnull=False
        )
        .values(
            msociety=F("pcn__request__society__name"),
            society_id=F("pcn__request__society_id"),
        )
        .distinct()
    )


def regional_society_paid_total(region, year):
    return (
        Bale.objects.filter(
            pcn__request__society__region_id=region,
            pcn__request__season_id=year,
            pcn__is_data_verified=True,
            primary_weight__isnull=False
        )
        .values("pcn__nill")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )


###########SOCIETY PER MARKET REPORT
def single_society_market_report_list(society, market, sale_no, season):
    return (
        Bale.objects.filter(
            Q(pcn__request__season_id=season)
            & Q(pcn__request__market_id=market)
            & Q(pcn__request__society_id=society)
            & Q(pcn__request__sales_number=sale_no)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
        )
        .values(
            pcnn=F("pcn__pcn_no"),
            mcenter=F("pcn__request__market__market_name"),
            saleno=F("pcn__request__sales_number"),
            saledate=F("pcn__request__sales_date"),
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('pcn__no')
    )


def single_society_market_report_total(society, market, saleno, season):
    return (
        Bale.objects.filter(
            Q(pcn__request__season_id=season)
            & Q(pcn__request__market_id=market)
            & Q(pcn__request__society_id=society)
            & Q(pcn__request__sales_number=saleno)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
        )
        .values("pcn__nill")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )
###########MARKET DECLARATION
def market_declaration_list_empty(society, market, saleno, season):
    return (
        Bale.objects.filter(
            pcn__request__season_id=season,
            pcn__request__market_id=market,
            pcn__request__society_id=society,
            pcn__request__sales_number=saleno
        )
        .values(
            pcnn=F("pcn__pcn_no"),
            mcenter=F("pcn__request__market__market_name"),
            saleno=F("pcn__request__sales_number"),
            saledate=F("pcn__request__sales_date"),
        )
        .annotate(
            kgp=Sum(
                Case(
                    When(ticket_id__isnull=False, then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesp=Count("id"),
            kgr=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesr=Sum(
                Case(
                    When(
                        Q(grade__grade_name__in=["R", "C"]),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            kgwthdrawn=Sum(
                Case(
                    When(Q(status="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            baleswthdrawn=Sum(
                Case(
                    When(Q(status="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
        ).order_by('pcn__no')
    )


###########MARKET DECLARATION
def market_declaration_list(society, market, saleno, season):
    return (
        Bale.objects.filter(
            pcn__request__season_id=season,
            pcn__request__market_id=market,
            pcn__request__society_id=society,
            pcn__request__sales_number=saleno,
            primary_weight__isnull=False
        )
        .values(
            pcnn=F("pcn__pcn_no"),
            mcenter=F("pcn__request__market__market_name"),
            saleno=F("pcn__request__sales_number"),
            saledate=F("pcn__request__sales_date"),
        )
        .annotate(
            kgp=Sum(
                Case(
                    When(ticket_id__isnull=False, then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesp=Count("id"),
            kgr=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesr=Sum(
                Case(
                    When(
                        Q(grade__grade_name__in=["R", "C"]),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            kgwthdrawn=Sum(
                Case(
                    When(Q(status="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            baleswthdrawn=Sum(
                Case(
                    When(Q(status="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
        ).order_by('pcn__no')
    )

def market_declaration_total_empty(society, market, saleno, season):
    return (
        Bale.objects.filter(
            pcn__request__season_id=season,
            pcn__request__market_id=market,
            pcn__request__society_id=society,
            pcn__request__sales_number=saleno,
        )
        .values(request_id01=F("pcn__request_id"))
        .annotate(
            kgp=Sum(
                Case(
                    When(ticket_id__isnull=False, then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesp=Count("id"),
            kgr=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesr=Sum(
                Case(
                    When(
                        Q(grade__grade_name__in=["R", "C"]),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            kgwthdrawn=Sum(
                Case(
                    When(Q(status="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            baleswthdrawn=Sum(
                Case(
                    When(Q(status="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
        )
    )


def market_declaration_total(society, market, saleno, season):
    return (
        Bale.objects.filter(
            pcn__request__season_id=season,
            pcn__request__market_id=market,
            pcn__request__society_id=society,
            pcn__request__sales_number=saleno,
            primary_weight__isnull=False,
        )
        .values(request_id01=F("pcn__request_id"))
        .annotate(
            kgp=Sum(
                Case(
                    When(ticket_id__isnull=False, then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesp=Count("id"),
            kgr=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesr=Sum(
                Case(
                    When(
                        Q(grade__grade_name__in=["R", "C"]),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            kgwthdrawn=Sum(
                Case(
                    When(Q(status="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            baleswthdrawn=Sum(
                Case(
                    When(Q(status="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
        )
    )


##################################
#####################
def grade_analysis_yearly(year, region):
    if region:
        bale=Bale.objects.filter(
            Q(pcn__request__season_id=year)
            &Q(pcn__request__society__region_id=region)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            &~Q(grade_id__isnull=True)
           
            &~Q(grade__grade_name__in=["R", "C", "W"])
        )
    else:
        bale=Bale.objects.filter(
            Q(pcn__request__season_id=year)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            &~Q(grade_id__isnull=True)
           
            &~Q(grade__grade_name__in=["R", "C", "W"])
        )


    
    return bale.values(gradename=F('grade__grade_name')).annotate(
        kgs=Sum(
            Case(
                When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                default=Value(0),
                output_field=FloatField(),
            )
        ),
        bales=Sum(
            Case(
                When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ),
        values=Sum(
            Case(
                When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                default=Value(0),
                output_field=FloatField(),
            )
        ),
    ).order_by('gradename')
    


def grade_analysis_yearly_total(year, region):
    if region:
        bale=Bale.objects.filter(
            Q(pcn__request__season_id=year)
            &Q(pcn__request__society__region_id=region)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            &~Q(grade_id__isnull=True)
           
            &~Q(grade__grade_name__in=["R", "C", "W"])
        )
    else:
        bale=Bale.objects.filter(
            Q(pcn__request__season_id=year)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            &~Q(grade_id__isnull=True)
     
            &~Q(grade__grade_name__in=["R", "C", "W"])
        )


    
    return bale.values('pcn__nill').annotate(
        kgs=Sum(
            Case(
                When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                default=Value(0),
                output_field=FloatField(),
            )
        ),
        bales=Sum(
            Case(
                When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ),
        values=Sum(
            Case(
                When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                default=Value(0),
                output_field=FloatField(),
            )
        ),
    ).order_by("-values")



#####################
def grade_analysis_per_society(society, year):
    return (
        Bale.objects.filter(
            Q(pcn__request__society_id=society)
            & Q(pcn__request__season_id=year)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
             &~Q(grade__grade_name__in=["R", "C", "W"])
        )
        .values(gradename=F('grade__grade_name'))
        .annotate(
            kgs=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            bales=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            values=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('gradename')
    )


def grade_analysis_per_society_total(society, year):
    return (
        Bale.objects.filter(
             Q(pcn__request__society_id=society)
            & Q(pcn__request__season_id=year)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
             &~Q(grade__grade_name__in=["R", "C", "W"])
        )
        .values("pcn__nill")
        .annotate(
            kgs=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            bales=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            values=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
       
    )

def current_buying_reports(year):
    return (
        Bale.objects.filter(
            Q(pcn__request__season_id=year)
 
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(grade_id__isnull=False)
        )
        .values(society_id=F("pcn__request__society_id"))
        .annotate(
            society=Max("pcn__request__society__name"),
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
             valueverified=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('society_id')
    )

def current_buying_reports_total( year):
    return (
        Bale.objects.filter(
           Q(pcn__request__season_id=year)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(grade_id__isnull=False)
        )
        .values("pcn__request__season_id")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            valueverified=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )
###ANALYSIS REPORT
def warehouse_verified_buying_reports(year):
    return (
        Bale.objects.filter(
            Q(pcn__request__season_id=year)
 
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(verified_grade_id__isnull=False)
        )
        .values(
            society=F("pcn__request__society__name"),
            society_id=F("pcn__request__society_id"),
           
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
             valueverified=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('valueb')
    )
def warehouse_verified_buying_reports_buyersummary(year):
    return (
        Bale.objects.filter(Q(created_on__gt='2022-05-30')&
            Q(pcn__request__season_id=year)
 
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(verified_grade_id__isnull=False)
            & Q(buyer_code__isnull=False)
        )
        .values('buyer_code' 
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
             valueverified=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('valueb')
    )
def warehouse_verified_buying_reports_per_buyer(year,buyer_code):
    return (
        Bale.objects.filter(Q(created_on__gt='2022-05-30')&
            Q(pcn__request__season_id=year)
            &Q(buyer_code=buyer_code)
 
            & Q(pcn__is_data_verified=True)
            
            & Q(primary_weight__isnull=False)
            & Q(verified_grade_id__isnull=False)
        )
        .values(
            society=F("pcn__request__society__name"),
            society_id=F("pcn__request__society_id"),
           
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
             valueverified=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('valueb')
    )
def warehouse_verified_buying_reports_total( year):
    return (
        Bale.objects.filter(Q(created_on__gt='2022-05-30')&
           Q(pcn__request__season_id=year)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(verified_grade_id__isnull=False)
        )
        .values("pcn__request__season_id")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            valueverified=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )
def warehouse_verified_buying_reports_total_per_buyer( year,buyer_code):
    return (
        Bale.objects.filter(
           Q(pcn__request__season_id=year)
           & Q(buyer_code=buyer_code)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(verified_grade_id__isnull=False)
        )
        .values("pcn__request__season_id")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name__in=["R", "C", "W"]), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            valueverified=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )

def shipped_value_comparison_report(year,type='all'):
    return (
        GeneralShipmentBale.objects.filter(
           Q(bale__pcn__request__season_id=year)&Q(general_shipment__is_closed_transporting=True)
        )
        .values(shid=F("general_shipment_id"),shipmentno=F("general_shipment__shipment_number"),
            fromw=F("general_shipment__from_warehouse__warehouse_name"),
             tow=F("general_shipment__to_warehouse__warehouse_name"),
            )
        .annotate(

            kgb=Sum(
                Case(
                    When(~Q(bale__grade__grade_name__in=["R", "C", "W"]), then="bale__primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(bale__grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(bale__grade__grade_name__in=["R", "C", "W"]), then="bale__value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            valueverified=Sum(
                Case(
                    When(~Q(bale__grade__grade_name="R") & ~Q(bale__grade__grade_name="W"), then="bale__verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
             shipmentkgb=Sum(
                Case(
                    When(~Q(bale__grade__grade_name__in=["R", "C", "W"]), then="transport_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            shipmentvalue=Sum(
                Case(
                    When(~Q(bale__grade__grade_name="R") & ~Q(bale__grade__grade_name="W"), then="bale__shipmentvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(bale__grade__grade_name__in=["R", "C"]), then="bale__primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(bale__grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('general_shipment__shipmentno')
    )
def shipped_value_comparison_report_total(year,type='all'):
    return (
        GeneralShipmentBale.objects.filter(
            Q(bale__pcn__request__season_id=year)&Q(general_shipment__is_closed_transporting=True)
        
        )
        .values(shid=F("bale__pcn__request__season_id")
            )
        .annotate(

            kgb=Sum(
                Case(
                    When(~Q(bale__grade__grade_name__in=["R", "C", "W"]), then="bale__primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(bale__grade__grade_name__in=["R", "C", "W"]), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(bale__grade__grade_name__in=["R", "C", "W"]), then="bale__value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            valueverified=Sum(
                Case(
                    When(~Q(bale__grade__grade_name="R") & ~Q(bale__grade__grade_name="W"), then="bale__verifiedvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
             shipmentkgb=Sum(
                Case(
                    When(~Q(bale__grade__grade_name__in=["R", "C", "W"]), then="transport_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            shipmentvalue=Sum(
                Case(
                    When(~Q(bale__grade__grade_name="R") & ~Q(bale__grade__grade_name="W"), then="bale__shipmentvalue"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(bale__grade__grade_name__in=["R", "C"]), then="bale__primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(bale__grade__grade_name__in=["R", "C"]), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )