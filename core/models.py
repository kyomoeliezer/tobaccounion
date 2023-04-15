from xmlrpc.client import boolean
from django.db import models
import uuid

# Create your models here.


class BaseDB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "auths.User", on_delete=models.CASCADE, null=True, blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Region(models.Model):
    region_name = models.CharField(max_length=500, null=True, blank=True)
    region_code = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        db_table = "region"

    def __str__(self):
        return self.region_name




class ProductGrade(BaseDB):
    grade_name = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product Grade"
        verbose_name_plural = "Product Grades"
        db_table = "product_grade"

    def __str__(self):
        return self.grade_name


class CropGrade(BaseDB):
    grade_name = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
   

    class Meta:
        verbose_name = "Crop Grade"
        verbose_name_plural = "Crop Grades"
        db_table = "crop_grade"

    def __str__(self):
        return self.grade_name


class Season(BaseDB):
    season_name = models.CharField(max_length=500, null=True, blank=True)
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)

    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
        db_table = "season"

    def __str__(self):
        return self.season_name

class ConstantCode(BaseDB):
    code_number = models.CharField(max_length=50)
    season=models.ForeignKey(Season,on_delete=models.DO_NOTHING,null=True)

    class Meta:
        verbose_name = "ConstantCode"
        verbose_name_plural = "ConstantCodes"
        db_table = "constant_code"

    def __str__(self):
        return self.code_number

class GradePrice(BaseDB):
    """database table for Grade Prices"""

    grade = models.ForeignKey(
        "CropGrade", on_delete=models.CASCADE, null=True, blank=True
    )
    season = models.ForeignKey(
        "Season", on_delete=models.CASCADE, null=True, blank=True
    )
    price = models.FloatField()

    class Meta:
        verbose_name = "GradePrice"
        verbose_name_plural = "GradePrices"
        db_table = "grade_price"

    def __str__(self):
        return self.grade.grade_name


class InHouseGrade(BaseDB):
    grade = models.CharField(max_length=500, null=True, blank=True)
    is_special =models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "InHouseGrade"
        verbose_name_plural = "InHouseGrades"
        db_table = "in_house_grade"

    def __str__(self):
        return self.grade


class CropSeed(BaseDB):
    seed_name = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "CropSeed"
        verbose_name_plural = "CropSeeds"
        db_table = "crop_seed"

    def __str__(self):
        return self.seed_name


class CropType(BaseDB):
    type_name = models.CharField(max_length=500, null=True, blank=True)
    crop_seed = models.ForeignKey(
        "CropSeed", verbose_name="crop_seed", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Crop Type"
        verbose_name_plural = "Crop Types"

    def __str__(self):
        return self.type_name


class WeightLoss(BaseDB):
    weight_loss = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "WeghtLoass"
        verbose_name_plural = "WeghtLoasss"

    def __str__(self):
        return str(self.weight_loss)
