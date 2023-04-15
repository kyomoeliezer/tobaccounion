from django.db import models
from core.models import BaseDB

# Create your models here.


class Association(BaseDB):
    """Primary Society"""
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    region = models.ForeignKey(
        "core.Region", verbose_name="region", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Association"
        verbose_name_plural = "Associations"
        db_table = "association"

    def __str__(self):
        return self.name


class Farmer(BaseDB):
    first_name = models.CharField(max_length=500, null=True, blank=True)
    middle_name = models.CharField(max_length=500, null=True, blank=True)
    last_name = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=500, null=True, blank=True)
    society = models.ForeignKey("Association", on_delete=models.CASCADE)
    farmer_code = models.CharField(max_length=500, null=True, blank=True)
    region = models.ForeignKey(
        "core.Region", verbose_name="region", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"
        db_table = "farmer"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
