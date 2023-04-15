from django.db import models
from core.models import BaseDB
from inventory.models import WAREHOUSE_SIZE_CHOICES

# Create your models here.


class ProcessingCentre(BaseDB):
    centre_name = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    centre_size = models.CharField(
        max_length=200,
        choices=WAREHOUSE_SIZE_CHOICES,
    )

    class Meta:
        verbose_name = "Processing Center"
        verbose_name_plural = "Processing Centre"
        db_table = "processing_centre"

    def __str__(self):
        return self.centre_name


class ProductCategory(BaseDB):
    category_name = models.CharField(max_length=500, null=True, blank=True)
    sub_category_of = models.ForeignKey(
        "ProductCategory", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "ProductCategory"
        verbose_name_plural = "ProductCategorys"
        db_table = "product_category"

    def __str__(self):
        return self.category_name


class ProductBale(BaseDB):
    bale_number = models.CharField(max_length=50, null=True, blank=True)
    bale_weight = models.IntegerField(null=True, blank=True)
    product_grade = models.ForeignKey(
        "core.ProductGrade", verbose_name="product_grade", on_delete=models.CASCADE
    )
    product_category = models.ForeignKey(
        "ProductCategory", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "ProductBale"
        verbose_name_plural = "ProductBales"
        db_table = "product_bale"

    def __str__(self):
        return self.bale_number


class ProductBaleInput(BaseDB):
    product_bale = models.ForeignKey(
        "ProductBale", on_delete=models.CASCADE, null=True, blank=True
    )
    bale = models.ForeignKey(
        "market.Bale", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "ProductBaleInput"
        verbose_name_plural = "ProductBaleInputs"
        db_table = "product_bale_input"

    def __str__(self):
        return self.product_bale.bale_number


class WasteBale(BaseDB):
    bale = models.ForeignKey(
        "market.Bale", related_name="waste_bale", on_delete=models.CASCADE
    )
    reason = models.CharField(max_length=5000)

    class Meta:
        verbose_name = "WasteBale"
        verbose_name_plural = "WasteBales"
        db_table = "waste_bale"

    def __str__(self):
        return self.bale.bale_number
