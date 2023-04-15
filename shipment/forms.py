from django import forms
from .models import *
from django.core.exceptions import ValidationError


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["full_name", "phone_number", "license",'company']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = TransportCompany
        fields = ["name", "address"]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-title'

        self.fields['address'].widget.attrs['rows'] = '2'
        self.fields['address'].widget.attrs['cols'] = '12'






class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ["track_name", "reg_number", "document_number",'company']


class WarehouseShipmentForm(forms.ModelForm):
    class Meta:
        model = WarehouseShipment
        fields = [
            "from_warehouse",
            "to_warehouse",
            "personnel",
            "personnel_receiver",
            "track",
            "driver",
            "shipment_date",
        ]


class MarketProcessingShipmentForm(forms.ModelForm):
    class Meta:
        model = MarketProcessingShipment
        fields = [
            "market",
            "processing_centre",
            "personnel",
            "market_request",
            "personnel_receiver",
            "track",
            "driver",
            "shipment_date",
        ]


class WarehouseProcessingShipmentForm(forms.ModelForm):
    class Meta:
        model = WarehouseProcessingShipment
        fields = [
            "warehouse",
            "processing_centre",
            "personnel",
            "personnel_receiver",
            "track",
            "driver",
            "shipment_date",
        ]


class MarketWarehouseShipmentForm(forms.ModelForm):
    class Meta:
        model = MarketWarehouseShipment
        fields = [
            "market",
            "warehouse",
            "track",
            "personnel",
            "market_request",
            "personnel_receiver",
            "driver",
            "shipment_date",
        ]


class SalesShipmentForm(forms.ModelForm):
    class Meta:
        model = SalesShipment
        fields = [
            "processing_centre",
            "sales_location",
            "track",
            "driver",
            "personnel",
            "shipment_date",
        ]
class GeneralShipmentForm(forms.ModelForm):
    shipment_date=forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = GeneralShipment
        fields = ['from_warehouse', 'to_warehouse', 'transporter', 'receiver', 'driver', 'track', 'shipment_date']

    def __init__(self, *args, **kwargs):
        super(GeneralShipmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-title'
      
        self.fields['from_warehouse'].widget.attrs['class'] = 'select2'
        self.fields['to_warehouse'].widget.attrs['class'] = 'select2'
        self.fields['transporter'].widget.attrs['class'] = 'select2'
        self.fields['driver'].widget.attrs['class'] = 'select2'
        self.fields['track'].widget.attrs['class'] = 'select2'
        self.fields['receiver'].widget.attrs['class'] = 'select2'

    def clean(self):
        clean_data=super(GeneralShipmentForm, self).clean()
        if clean_data['from_warehouse'] == clean_data['to_warehouse']:
            raise ValidationError('Cannote be shiped to the same warehouse')

class GeneralEmailForm(forms.ModelForm):
    class Meta:
        model = SendingShipmentEmail
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(GeneralEmailForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-title'



