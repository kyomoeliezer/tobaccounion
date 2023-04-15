from django import template
from django.db.models import Max, Min
from market.models import *
from core.models import *
from shipment.models import MarketWarehouseShipmentBale
from django.db.models import *  #
import datetime

register = template.Library()


@register.simple_tag
def int_compare(a, b):
    if a and b:
        # if is_interger(a) and b.is_interger(b):
        if a == b:
            return True
        else:
            return False
    else:
        return False


@register.simple_tag
def product(a, b):
    if a and b:
        return float(a) * float(b)
    else:
        return b


@register.simple_tag
def divd(a, b):
    if a and b:
        return float(a) / float(b)
    else:
        return 0


@register.simple_tag
def set(a):
    if a:
        return float(a)
    else:
        return 0


@register.simple_tag
def set_str(a):
    return a


@register.simple_tag
def translate(status):
    if "R" in status:
        return "Rejected"
    elif "W" in status:
        return "Withdrawn"
    elif "C" in status:
        return "Cancelled"
    else:
        return "OK"


@register.simple_tag
def toa(a, b):
    if a and b:
        return float(b) - float(a)
    elif a and not b:
        return -float(a)
    elif b and not a:
        return float(b)
    else:
        return 0


@register.simple_tag
def toa2(a, b):
    if a and b and a != 0:
        return float(b) - float(a)
    elif a and b and a == 0:
        return float(a)
    else:
        return 0


@register.simple_tag
def current_sesson():
    date = datetime.datetime.today().date()
    current = Season.objects.filter(end_date__gte=date, start_date__lte=date).last()
    if current:
        return current
    else:
        return None


@register.simple_tag
def box_tickets(box_id):
    max_ = Ticket.objects.filter(batch__box_id=box_id).aggregate(tno=Count("id"))
    if max_:
        return max_["tno"]
    else:
        return ""


@register.simple_tag
def buyer_name(code):
    code=code.replace(" ", "")
    buyer_ = Buyer.objects.filter(buyer_code=code).first()
    if buyer_:
        return buyer_.full_name
    else:
        return ""

@register.simple_tag
def first_box_ticket(Prequest_id):
    min_ = Ticket.objects.filter(batch_id=btch_id).aggregate(tno=Min("ticket_no"))
    if min_:
        return min_["tno"]
    else:
        return ""


@register.simple_tag
def last_box_ticket(btch_id):
    max_ = Ticket.objects.filter(batch_id=btch_id).aggregate(tno=Max("ticket_no"))
    if max_:
        return max_["tno"]
    else:
        return ""


@register.simple_tag
def first_batch(boxid):
    min_ = Batch.objects.filter(box_id=boxid).aggregate(bno=Min("batch_no"))
    if min_:
        return min_["bno"]
    else:
        return ""


@register.simple_tag
def last_batch(boxid):
    max_ = Batch.objects.filter(box_id=boxid).aggregate(bno=Max("batch_no"))
    if max_:
        return max_["bno"]
    else:
        return ""


@register.simple_tag
def grade_name(id):
    g = CropGrade.objects.filter(id=id).first()
    if g:
        return g.grade_name
    else:
        return ""


@register.simple_tag
def get_transport_weight(bale_id):
    baleship = MarketWarehouseShipmentBale.objects.filter(bale_id=bale_id)
    if baleship:
        return baleship.first().transport_weight
    else:
        return ""


@register.simple_tag
def get_rcvd_weight(bale_id):
    baleship = MarketWarehouseShipmentBale.objects.filter(bale_id=bale_id)
    if baleship:
        return baleship.first().received_weight
    else:
        return ""


@register.simple_tag
def request_is_free(pk):
    return Bale.objects.filter(pcn__request_id=pk, pcn__data_input="completed").exists()


@register.simple_tag
def get_tickets(pcn_id):
    return Bale.objects.filter(pcn_id=pcn_id).order_by("created_on")


@register.simple_tag
def get_ticket_total(pcn_id):
    trans = MarketWarehouseShipmentBale.objects.filter(bale__pcn_id=pcn_id).aggregate(
        t_weight=Sum("transport_weight"), r_weight=Sum("received_weight")
    )
    t_weight = r_weight = 0
    if trans["t_weight"]:
        t_weight = trans["t_weight"]

    if trans["r_weight"]:
        r_weight = trans["r_weight"]

    return (
        Bale.objects.filter(Q(pcn_id=pcn_id) & ~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"))
        .values(
            pcnn=F("pcn__pcn_no"),
            pcn_nid=F("pcn_id"),
            mname=F("pcn__request__market__market_name"),
            societyname=F("pcn__request__society__name"),
        )
        .annotate(
            count=Count("id"),
            weight_t=Sum("primary_weight"),
            tt_weight=Value(t_weight, FloatField()),
            weight_rcvd=Value(r_weight, FloatField()),
            value_t=Sum("value"),
        )
    )

@register.simple_tag
def bale_value(grade_id,weight,year_id):
    if weight:
        gradepriceob=GradePrice.objects.filter(grader_id=grade_id,season_id=year_id).first()
        if gradepriceob:
            return round(float(weight)*gradepriceob.price,2)
    return 0


@register.simple_tag
def society_paid_list(society, year):
    return (
        Bale.objects.filter(
            pcn__request__society_id=society,
            pcn__request__season_id=year,
            pcn__is_data_verified=True,
        )
        .values(
            mcenter=F("pcn__request__market__market_name"),
            saleno=F("pcn__request__sales_number"),
            saledate=F("pcn__request__sales_date"),
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name="R"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name="R"), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )



@register.simple_tag
def society_paid_total(society, year):
    return (
        Bale.objects.filter(
            pcn__request__society_id=society,
            pcn__request__season_id=year,
            pcn__is_data_verified=True,
        )
        .values("pcn__nill")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="value"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            kgdedu=Sum(
                Case(
                    When(Q(grade__grade_name="R"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name="R"), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )


@register.simple_tag
def count_ticket(pk):
    return Bale.objects.filter(pcn__request_id=pk).count()


@register.simple_tag
def last_batch(boxid):
    max_ = Batch.objects.filter(box_id=boxid).aggregate(bno=Max("batch_no"))
    if max_:
        return max_["bno"]
    else:
        return ""


@register.simple_tag
def min_ticket(request_id):
    if Bale.objects.filter(market_request_id=request_id).first():

        baleob = Bale.objects.filter(market_request_id=request_id).earliest("created_on")
        if baleob:
            return baleob.ticket.ticket_number
    return ""


@register.simple_tag
def max_ticket(request_id):
    if Bale.objects.filter(market_request_id=request_id).first():

        baleob = Bale.objects.filter(market_request_id=request_id).latest("created_on")
        if baleob:
            return baleob.ticket.ticket_number
    return ""


@register.simple_tag
def society_buying_report(society, year):
    return (
        Bale.objects.filter(
            
             Q(pcn__request__season_id=year)
            &Q(pcn__request__society_id=society)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(grade_id__isnull=False)
        )
        .values(
            mcenter=F("pcn__request__market__market_name"),
            saleno=F("pcn__request__sales_number"),
            saledate=F("pcn__request__sales_date"),
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="value"),
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
                    When(Q(grade__grade_name="R"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name="R"), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        ).order_by('saleno')
    )


@register.simple_tag
def society_paid_list_verified(society, year):
    return (
        Bale.objects.filter(
            
             Q(pcn__request__season_id=year)
                & Q(pcn__request__society_id=society)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(verified_grade_id__isnull=False)
        )
        .values(
            mcenter=F("pcn__request__market__market_name"),
            saleno=F("pcn__request__sales_number"),
            saledate=F("pcn__request__sales_date"),
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="value"),
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
                    When(Q(grade__grade_name="R"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name="R"), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )

@register.simple_tag
def society_paid_list_verified_per_buyer(society, year,bcode):
    return (
        Bale.objects.filter(
            
             Q(pcn__request__season_id=year)
                & Q(pcn__request__society_id=society)
                & Q(buyer_code=bcode)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(verified_grade_id__isnull=False)
        )
        .values(
            mcenter=F("pcn__request__market__market_name"),
            saleno=F("pcn__request__sales_number"),
            saledate=F("pcn__request__sales_date"),
        )
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="value"),
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
                    When(Q(grade__grade_name="R"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name="R"), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )


@register.simple_tag
def society_paid_total_verified(society, year):
    return (
        Bale.objects.filter(
           Q(pcn__request__season_id=year)
            & Q(pcn__is_data_verified=True)
            & Q(primary_weight__isnull=False)
            & Q(verified_grade_id__isnull=False)
        )
        .values("pcn__nill")
        .annotate(
            kgb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            valueb=Sum(
                Case(
                    When(~Q(grade__grade_name="R") & ~Q(grade__grade_name="W"), then="value"),
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
                    When(Q(grade__grade_name="R"), then="primary_weight"),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
            balesdedu=Sum(
                Case(
                    When(Q(grade__grade_name="R"), then=Value(1)),
                    default=Value(0),
                    output_field=FloatField(),
                )
            ),
        )
    )