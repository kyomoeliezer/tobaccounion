from django import forms
from .models import *


class ProcessingCentreForm(forms.ModelForm):
    class Meta:
        model = ProcessingCentre
        fields = ["centre_name", "location", "centre_size"]
