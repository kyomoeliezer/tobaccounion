from auths.auth_token import GlobalAuth
from inventory import schemas
from .views import *
from ninja import Router
from typing import List

api = Router(auth=GlobalAuth())


# @api.post("/add-warehouse", response=schemas.WarehouseSchema)
# def add_warehouse(request, warehouse: schemas.CreateWarehouseSchema):
#     return Warehouse.create_warehouse(request, warehouse)


@api.get("/get-warehouses", response=List[schemas.WarehouseSchema])
def get_warehouses(request):
    return Warehouse.get_warehouses(request)


# @api.delete("/delete-warehouse")
# def delete_warehouse(request, id: str):
#     return Warehouse.delete_warehouse(request, id)


# @api.post("/add-warehouse-section", response=schemas.WarehouseSectionSchema)
# def add_warehouse_section(
#     request, warehouse_section: schemas.CreateWarehouseSectionSchema
# ):
#     return WarehouseSection.create_warehouse_section(request, warehouse_section)


@api.get("/get-warehouse-sections", response=List[schemas.WarehouseSectionSchema])
def get_warehouse_sections(request):
    return WarehouseSection.get_warehouse_sections(request)


# @api.delete("/delete-warehouse-section")
# def delete_warehouse_section(request, id: str):
#     return WarehouseSection.delete_warehouse_section(request, id)


@api.patch("/update-warehouse-bale")
def update_warehouse_bale(request, warehouse_bale_schema: schemas.WarehouseBaleSchema):
    return WarehouseBale.update_warehouse_bale(request, warehouse_bale_schema)
