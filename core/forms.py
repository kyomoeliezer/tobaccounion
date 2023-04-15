from dataclasses import fields
from django import forms
from .models import *


class Region(forms.ModelForm):
    class Meta:
        model = Region
        fields = ["region_name", "region_code"]


class ConstantCodeForm(forms.ModelForm):
    class Meta:
        model = ConstantCode
        fields = ["code_number",'season']


class GradeForm(forms.ModelForm):
    class Meta:
        model = CropGrade
        fields = ["grade_name"]


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ["season_name", "start_date", "end_date"]


class InHouseGradeForm(forms.ModelForm):
    class Meta:
        model = InHouseGrade
        fields = ["grade","is_special"]


class ProductGradeForm(forms.ModelForm):
    class Meta:
        model = ProductGrade
        fields = ["grade_name"]


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ["season_name", "start_date", "end_date"]


class GradePriceForm(forms.ModelForm):
    class Meta:
        model = GradePrice
        fields = ["grade", "price", "season"]
