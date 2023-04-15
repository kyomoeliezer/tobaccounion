from django.shortcuts import render,HttpResponse
from core.models import CropGrade

from inventory import models
# from market.views import Bale
from market.models import Bale as warehouse_bale

# Create your views here.


class Warehouse:
    def __init__(self):
        pass

    def create_warehouse(request, create_warehouse_schema):
        try:
            if type(create_warehouse_schema) != "dict":
                create_warehouse_schema = create_warehouse_schema.dict()

            warehouse = models.Warehouse.objects.create(**create_warehouse_schema)
            warehouse.save()
            return warehouse
        except:
            raise "Internal Server Error"

    def get_warehouses(request):
        try:
            warehouses = models.Warehouse.objects.filter(is_active=True)
            return warehouses
        except:
            raise "Internal Server Error"

    def delete_warehouse(request, id: str):
        try:
            warehouse = models.Warehouse.objects.filter(id=id)
            if warehouse:
                warehouse.update(is_active=False)
                return "Warehouse was successful Deleted"
            return "Warehouse was not found, may be was aleady deleted"
        except:
            raise "Internal Server Error"


class WarehouseSection:
    def __init__(self):
        pass

    def create_warehouse_section(request, create_warehouse_schema):
        try:
            if type(create_warehouse_schema) != "dict":
                create_warehouse_schema = create_warehouse_schema.dict()
            create_warehouse_schema["warehouse"] = models.Warehouse.objects.get(
                id=create_warehouse_schema["warehouse"]
            )
            warehouse_section = models.WarehouseSection.objects.create(
                **create_warehouse_schema
            )
            warehouse_section.save()
            return warehouse_section
        except:
            raise "Internal Server Error"

    def get_warehouse_sections(request):
        try:
            warehouse_sections = models.WarehouseSection.objects.filter(is_active=True)
            return warehouse_sections
        except:
            raise "Internal Server Error"

    def delete_warehouse_section(request, id: str):
        try:
            warehouse_section = models.WarehouseSection.objects.filter(id=id)
            if warehouse_section:
                warehouse_section.update(is_active=False)
                return "Warehose Section was successful Deleted"
            return "No warehouse section was found, may be already deleted"
        except:
            raise "Internal Server Error"


class WarehouseBale:
    def __init__(self):
        pass

    def update_warehouse_bale(request, edit_bale_schema):
        if type(edit_bale_schema) != "dict":
            edit_bale_schema = edit_bale_schema.dict()
        if edit_bale_schema["warehouse"]:
            edit_bale_schema["warehouse"] = models.Warehouse.objects.get(
                id=edit_bale_schema["warehouse"]
            )
        else:
            edit_bale_schema["warehouse"] = None

        if edit_bale_schema["current_grade"]:
            edit_bale_schema["current_grade"] = CropGrade.objects.get(
                id=edit_bale_schema["current_grade"]
            )
        else:
            edit_bale_schema["current_grade"] = None

        if edit_bale_schema["verified_grade"]:
            edit_bale_schema["verified_grade"] = CropGrade.objects.get(
                id=edit_bale_schema["verified_grade"]
            )
        else:
            edit_bale_schema["verified_grade"] = None

        bale = warehouse_bale.objects.filter(id=edit_bale_schema["id"])
        edit_bale_schema.pop("id")
        bale.update(**edit_bale_schema)
        return edit_bale_schema
