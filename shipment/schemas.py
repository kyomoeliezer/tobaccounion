from uuid import UUID
from venv import create
from ninja.orm import create_schema
from ninja import Schema
from typing import List
from shipment.models import (
    MarketProcessingShipment,
    MarketProcessingShipmentBale,
    MarketWarehouseShipment,
    MarketWarehouseShipmentBale,
    SalesShipment,
    WarehouseProcessingShipment,
    WarehouseProcessingShipmentBale,
    WarehouseShipment,
    WarehouseShipmentBale,
)
import uuid
from typing import List


WarehouseShipmentBaleSchema = create_schema(WarehouseShipmentBale)
CreateWarehouseShipmentBaleSchema = create_schema(
    WarehouseShipmentBale,
    exclude=["created_on", "updated_on", "created_by", "is_active"],
)

MarketWarehouseShipmentBaleSchema = create_schema(MarketWarehouseShipmentBale)
CreateMarketWarehouseShipmentBaleSchema = create_schema(
    MarketWarehouseShipmentBale,
    exclude=["created_on", "updated_on", "created_by", "is_active"],
)

MarketProcessingShipmentBaleSchema = create_schema(MarketProcessingShipmentBale)
CreateMarketProcessingShipmentSchema = create_schema(
    MarketProcessingShipmentBale,
    exclude=["created_on", "updated_on", "created_by", "is_active"],
)

WarehouseProcessingShipmentBaleSchema = create_schema(WarehouseProcessingShipmentBale)
CreateWarehouseProcessingShipmentSchema = create_schema(
    WarehouseProcessingShipmentBale,
    exclude=["created_on", "updated_on", "created_by", "is_active"],
)

SalesShipmentSchema = create_schema(SalesShipment)
CreateSalesShipmentSchema = create_schema(
    SalesShipment, exclude=["id", "created_on", "updated_on", "created_by", "is_active"]
)


class MarketWarehouseDataSchema(Schema):
    shipment_number: str
    market: str
    warehouse: str
    market_request: str
    sales_number: int = 0 or None
    shipment_bales: List

class CustomShpmentDataSchema(Schema):
    shipment_id: str
    shipment_type: str
    from_warehouse: str
    to_warehouse: str
    total_tickets:int = 0 or None
    total_transport_weight: float = 0.0 or None
    total_receiving_weight: float = 0.0 or None

class TicketForShipmentDataSchema(Schema):
    bale_id: uuid.UUID = "" or None
    ticket_number: str = "" or None
    shipment_id: uuid.UUID = "" or None
    shipment_type: str ="" or None
    primary_weight: float = 0.0 or None
    current_weight: float = 0.0 or None
    grade: uuid.UUID= "" or None
    in_house_grade: uuid.UUID = "" or None
    transport_weight: float = 0.0 or None
    receiving_weight: float = 0.0 or None

class EditShipmentBAleDataSchema(Schema):
    bale_id: uuid.UUID = "" or None
    grade: str = "" or None
    in_house_grade: str = "" or None
    shipment_id: uuid.UUID = "" or None
    transport_weight: float = 0.0 or None
    receiving_weight: float = 0.0 or None
    shipment_type:str =""




class MarketProcessingDataSchema(Schema):
    shipment_number: str
    market: str
    processing_centre: str
    market_request: str
    sales_number: int = 0 or None
    shipment_bales: List


class WarehouseDataSchema(Schema):
    shipment_number: str
    from_warehouse: str
    to_warehouse: str
    shipment_bales: List


class WarehouseProcessingDataSchema(Schema):
    shipment_number: str
    warehouse: str
    processing_centre: str
    shipment_bales: List


class EditShipmentBaleSchema(Schema):
    id: UUID or None
    transport_weight: float or None
    received_weight: float or None
