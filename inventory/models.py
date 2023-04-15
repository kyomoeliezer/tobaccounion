from django.db import models
from model_utils import Choices
from core.models import BaseDB

# Create your models here.
WAREHOUSE_SIZE_CHOICES = Choices(
    ("SMALL", "Small"), ("MEDIUM", "Mediau"), ("LARGE", "Large")
)


class Warehouse(BaseDB):
    warehouse_name = models.CharField(max_length=500, null=True, blank=True)
    region = models.ForeignKey(
        "core.Region", verbose_name="region", on_delete=models.CASCADE
    )
    #is_for_sold_or_process=models.CharField(default='yes',null=True,blank=True,max_length=30)
    warehouse_size = models.CharField(
        max_length=200,
        choices=WAREHOUSE_SIZE_CHOICES,
    )

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"
        db_table = "warehouse"

    def __str__(self):
        return self.warehouse_name


class WarehouseSection(BaseDB):
    section_name = models.CharField(max_length=500, null=True, blank=True)
    warehouse = models.ForeignKey(
        "Warehouse", verbose_name="warehouse", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "WarehouseSection"
        verbose_name_plural = "WarehouseSections"
        db_table = "warehouse_section"

    def __str__(self):
        return self.section_name


class WarehouseBale(BaseDB):
    Warehouse = models.ForeignKey("Warehouse", on_delete=models.CASCADE)
    warehouse_section = models.ForeignKey(
        "WarehouseSection", on_delete=models.CASCADE, null=True, blank=True
    )
    bale = models.ForeignKey("market.Bale", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "WarehouseBale"
        verbose_name_plural = "WarehouseBales"
        db_table = "warehouse_bale"

    def __str__(self):
        return self.Warehouse.warehouse_name
