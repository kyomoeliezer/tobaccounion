from auths.auth_token import GlobalAuth
from ninja import Router
from .views import *
from shipment import schemas
from typing import List

# API router
api = Router(auth=GlobalAuth())


@api.get(
    "/load-market-warehouse-bales",
    response=schemas.MarketWarehouseDataSchema,
)
def load_market_warehouse_bales(request):
    return Shipment.load_market_to_warehouse_shipment_bales(request)


@api.patch("/update-market-warehouse-bales")
def update_market_warehouse_bales(request, bales: List[schemas.EditShipmentBaleSchema]):
    return Shipment.update_market_to_warehouse_shipment_bales(bales)


@api.get(
    "/load-market-processing-bales",
    response=schemas.MarketProcessingDataSchema,
)
def load_market_processing_bales(request):
    return Shipment.load_market_to_processing_shipment_bales(request)


@api.patch("/update-market-processing-bales")
def update_market_processing_bales(
    request, bales: List[schemas.EditShipmentBaleSchema]
):
    return Shipment.update_market_to_processing_shipment_bales(bales)


@api.get(
    "/load-warehouse-to-warehouse-bales",
    response=schemas.WarehouseDataSchema,
)
def load_warehouse_warehouse_bales(request):
    return Shipment.load_warehouse_to_warehouse_shipment_bales(request)


@api.patch("/update-warehouse-to-warehouse-bales")
def update_warehouse_warehouse_bales(
    request, bales: List[schemas.EditShipmentBaleSchema]
):
    return Shipment.update_warehouse_to_warehouse_shipment_bales(bales)


@api.get(
    "/load-warehouse-processing-bales",
    response=schemas.WarehouseProcessingDataSchema,
)
def load_warehouse_processing_bales(request):
    return Shipment.load_warehouse_to_processing_shipment_bales(request)


@api.patch("/update-warehouse-processing-bales")
def update_warehouse_processing_bales(
    request, bales: List[schemas.EditShipmentBaleSchema]
):
    return Shipment.update_warehouse_to_processing_shipment_bales(bales)


@api.patch("/end-warehouse-processing-loading")
def end_warehouse_processing_loading(request):
    return Shipment.end_warehouse_processing_loading(request)


@api.patch("/end-warehouse-processing-receiving")
def end_warehouse_processing_receiving(request):
    return Shipment.end_warehouse_processing_receiving(request)


@api.patch("/end-warehouse-to-warehouse-loading")
def end_warehouse_to_warehouse_loading(request):
    return Shipment.end_warehouse_warehouse_loading(request)


@api.patch("/end-warehouse-to-warehouse-receiving")
def end_warehouse_to_warehouse_receiving(request):
    return Shipment.end_warehouse_warehouse_receiving(request)


@api.patch("/end-market-processing-loading")
def end_market_processing_loading(request):
    return Shipment.end_market_processing_loading(request)


@api.patch("/end-market-processing-receiving")
def end_market_processing_receiving(request):
    return Shipment.end_market_processing_receiving(request)


@api.patch("/end-market-warehouse-loading")
def end_market_warehouse_loading(request):
    return Shipment.end_market_warehouse_loading(request)


@api.patch("/end-market-warehouse-receiving")
def end_market_warehouse_receiving(request):
    return Shipment.end_market_warehouse_receiving(request)

"""BALES FOR CUSTOM SHIPMENT"""
@api.get("/load-custom-shipment",response=schemas.CustomShpmentDataSchema,)
def load_custom_shipment(request):
    return Shipment.load_custom_shipment(request)


@api.get("/get-ticket-for-shipment",response=schemas.TicketForShipmentDataSchema,)
def get_ticket_for_shipment(request,ticket_number):
    return Shipment.get_ticket_for_shipment(request,ticket_number)

@api.patch("/add-update-bale-for-shipment")
def add_update_bale_for_shipment(request,bale: schemas.EditShipmentBAleDataSchema):
    return Shipment.add_update_bale_for_shipment(request,bale)

"""BALES FOR CUSTOM SHIPMENT"""