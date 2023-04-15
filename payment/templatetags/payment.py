from django import template
from django.db.models import *
from market.models import *
from core.models import *
from shipment.models import MarketWarehouseShipmentBale
from django.db.models import *  #
import datetime
from payment.models import Payment

register = template.Library()

@register.simple_tag
def paid(socity_id):
    data= Payment.objects.filter(society_id=socity_id,is_canceled=False).aggregate(paid=Sum('amount'))
    if data['paid']:
        return data['paid']
    else:
        return None

@register.simple_tag
def paid_total():
    data= Payment.objects.filter(is_canceled=False).aggregate(paid=Sum('amount'))
    if data['paid']:
        return data['paid']
    else:
        return None
@register.simple_tag
def toa_now(m1,m2):
    if m1 and m2:
        return float(m1) - float(m2)

    elif m1 and not m2:

        return float(m1)

    elif not m1 and m2:

        return float(m2)
    else:
        return 0

@register.simple_tag
def set(no):
    return no