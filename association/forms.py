from django import forms
from .models import *


class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "farmer_code",
            "phone_number",
            "society",
            "region",
        ]


class SocietyForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = ["name", "region"]
