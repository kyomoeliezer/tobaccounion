from django import forms
from .models import *
from market.models import Bale


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["warehouse_name", "region", "warehouse_size"]


class WarehouseSectionForm(forms.ModelForm):
    class Meta:
        model = WarehouseSection
        fields = ["section_name", "warehouse"]


class RegradingForm(forms.ModelForm):
    class Meta:
        model = Bale
        fields = ["buyer_code",]