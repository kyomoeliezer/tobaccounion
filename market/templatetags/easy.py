from django import template
from django.db.models import Max, Min
from market.models import *
from core.models import *
from shipment.models import MarketWarehouseShipmentBale,GeneralShipmentBale,GeneralShipmentReceivedBales
from django.db.models import *  #
import datetime

register = template.Library()



@register.simple_tag
def extra_primary():
    return Bale.objects.filter(primary_weight__gt=90).count()

@register.simple_tag
def extra_transport():
    return MarketWarehouseShipmentBale.objects.filter(Q(transport_weight__gt=90)|Q(received_weight__gt=90)).count()

@register.simple_tag
def extra_processing():
    return GeneralShipmentBale.objects.filter(Q(transport_weight__gt=90)|Q(receiving_weight__gt=90)).count()
 
@register.simple_tag
def has_no_data(market_ticket_request_id):
    return Bale.objects.filter(Q(market_request_id=market_ticket_request_id)&Q(farmer_id__isnull=False)&Q(Q(primary_weight=0)|Q(primary_weight__isnull=False))&Q(grade_id__isnull=False)).exists()

@register.simple_tag
def is_latest(market_ticket_request_id):
    data=MarketTicketRequest.objects.latest('created_on')#Bale.objects.filter(Q(market_request_id=market_ticket_request_id)&Q(farmer_id__isnull=False)&Q(Q(primary_weight=0)|Q(primary_weight__isnull=False))&Q(grade_id__isnull=False)).exists()
    if data.id == market_ticket_request_id:
        return True
    else:
        return False

@register.simple_tag
def receiving_data(ship_id):
    return GeneralShipmentReceivedBales.objects.filter(general_shipment_id=ship_id).aggregate(
        Rweight=Sum('receiving_weight'),nbales=Count('id')
    )

@register.simple_tag
def receiving_data_total():
    return GeneralShipmentReceivedBales.objects.aggregate(
        Rweight=Sum('receiving_weight'),nbales=Count('id')
    )



