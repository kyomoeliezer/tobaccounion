from inventory.models import Warehouse, WarehouseSection
from ninja.orm import create_schema
from ninja import Schema
import uuid

WarehouseSchema = create_schema(Warehouse)
CreateWarehouseSchema = create_schema(
    Warehouse, exclude=["id", "created_on", "updated_on"]
)


WarehouseSectionSchema = create_schema(WarehouseSection)
CreateWarehouseSectionSchema = create_schema(
    WarehouseSection, exclude=["id", "created_on", "updated_on"]
)


class WarehouseBaleSchema(Schema):
    id: uuid.UUID = "" or None
    warehouse: uuid.UUID = "" or None
    current_grade: uuid.UUID = "" or None
    verified_grade: uuid.UUID = "" or None
    current_weight: float = 0.0 or None
