from django.urls import path, re_path
from . import web

app_name = "inventory"
urlpatterns = [
    path("warehouses/", web.Warehouse.get_warehouses, name="warehouses"),
    path("add-warehouse/", web.AddWarehouseView.as_view(), name="add-warehouse"),
    re_path(r"^warehouse/(?P<pk>[\w-]+)/", web.UpdateWarehouseView.as_view(), name="edit-warehouse"),

    ####REGRADING
    ######REGRADING
    re_path(r"^regrading$", web.RegradingList.as_view(), name="regrading"),
    re_path(
        r"^delete-warehouse/(?P<warehouse_id>[\w-]+)/$",
        web.Warehouse.delete_warehouse,
        name="delete-warehouse",
    ),
]
