from django import forms
from .models import *
from shipment.models import MarketWarehouseShipmentBale,GeneralShipmentBale
from inventory.models import Warehouse
from association.models import Association
from core.models import *


class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ["market_name", "market_code", "region"]


class PrintRequestForm(forms.ModelForm):
    last_ticket=forms.IntegerField()
    initial_ticket = forms.IntegerField()
    class Meta:
        model = PrintRequest
        fields = ["request_name", "number_of_tickets","initial_ticket","last_ticket","is_mannual"]




    def clean_initialticket(self):
        initial_ticket = self.cleaned_data["initialticket"]
        startstr=str(initial_ticket)

        if  not len(startstr) == 6 or not startstr.startswith( '1' ):
            raise forms.ValidationError('Initial ticket must start with 1 and must not be less than 6 characters ')

        return initial_ticket

    def clean_lastticket(self):
        last_ticket = self.cleaned_data["lastticket"]
        startstr=str(last_ticket)

        if  not len(startstr) == 6 or not startstr.startswith( '1' ):
            raise forms.ValidationError('Last ticket must start with 1 and must not be less than 6 characters ')
        return last_ticket





class MarketTicketRequestForm(forms.ModelForm):
    class Meta:
        model = MarketTicketRequest
        fields = [
            "ticket_request_name",
            "market",
            "society",
            "number_of_tickets",
            "sales_date",
            "personnel",
            "season",
            "mobile_clerk",
            'is_mannual',
        ]


class EditMarketTicketRequestForm(forms.ModelForm):
    class Meta:
        model = MarketTicketRequest
        fields = [
            "ticket_request_name",
            "market",
            "society",
            "sales_date",
            "personnel",
            "season",
            "mobile_clerk",
            "sales_number",
            "is_mannual",
        ]

class UpdateTicketUsingTicketNoForm(forms.ModelForm):

    grade=forms.ModelChoiceField(queryset = CropGrade.objects.all(),label='Farmer Grade' )
    verified_grade=forms.ModelChoiceField(queryset = CropGrade.objects.all(),label='Verified Grade' )
    society=forms.ModelChoiceField(queryset = Association.objects.all(),label='Primary Society' )
    market=forms.ModelChoiceField(queryset = Market.objects.all(),label='Market' )
    in_house_grade=forms.ModelChoiceField(queryset = InHouseGrade.objects.all(),label='Inhouse Grade' )
    primary_weight=forms.FloatField(required=False, max_value=100, min_value=0,widget=forms.NumberInput(attrs={'id': 'fd', 'step': "0.01"}),label='Farmer Weight') 
    current_weight=forms.FloatField(required=False, max_value=100, min_value=0,widget=forms.NumberInput(attrs={'id': 'fd1', 'step': "0.01"}),label='Warehouse Weight') 
    buyer=forms.ModelChoiceField(queryset = Buyer.objects.all(),label='Market Buyer Code' )
    verifier=forms.ModelChoiceField(queryset = GradeVerifier.objects.all(),label='Warehouse Verifier')
    warehouse=forms.ModelChoiceField(queryset = Warehouse.objects.all(),label='Warehouse')
    ticket_number=forms.IntegerField(required=True,max_value=239000,min_value=230001,label='Ticket Number')
    nill=forms.CharField(required=False)

    class Meta:
        model = Pcn
        fields = ['nill',]


class TicketReleaseForm(forms.ModelForm):
    first = forms.IntegerField(required=True, label="FIRST TICKET")
    last = forms.IntegerField(required=True, label="LAST TICKET")

    class Meta:
        model = Pcn
        fields = [
            "nill",
        ]

class AdditionalTicketForm(forms.ModelForm):
    no_tickets = forms.IntegerField(required=True, label="FIRST TICKET")

    class Meta:
        model = Pcn
        fields = [
            "nill",
        ]


class MarketTicketRequestPersonnelForm(forms.ModelForm):
    class Meta:
        model = MarketTicketRequestPersonnel
        fields = ["personnel", "market_ticket_request"]


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ["full_name", "buyer_code"]

class VerifyForm(forms.ModelForm):
    class Meta:
        model = GradeVerifier
        fields = ["full_name", "code"]

class BaleForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["ticket_number"]

class BaleEditForm(forms.ModelForm):
    class Meta:
        model = Bale
        fields = ["primary_weight"]

class BaleEditMarketWarehouse(forms.ModelForm):
    class Meta:
        model = MarketWarehouseShipmentBale
        fields = ["transport_weight","received_weight"]

class BaleEditGeneralShipmentWarehouse(forms.ModelForm):
    class Meta:
        model = GeneralShipmentBale
        fields = ["transport_weight","receiving_weight"]

