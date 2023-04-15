from django import forms
from .models import *
from core.models import *
from association.models import *
from market import models as market_models


class PcnReportForm(forms.ModelForm):
    market = forms.ModelChoiceField(
        queryset=market_models.Market.objects.all(),
        widget=forms.Select(attrs={"class": "select2", "id": "market_id"}),
    )
    primary_society = forms.ModelChoiceField(
        queryset=Association.objects.all(),
        widget=forms.Select(attrs={"class": "select2", "id": "society_id"}),
    )
    sale_no = forms.CharField(
        required=True,
        label="Sale no",
        widget=forms.TextInput(attrs={"class": "saleno_id"}),
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        widget=forms.Select(attrs={"class": "select2", "id": "season_id"}),
    )
    nill = forms.CharField(required=False)
    post_type = forms.CharField(required=False)

    no = forms.CharField(required=False)

    class Meta:
        model = market_models.Pcn
        fields = ("nill",)


class PerSocietyReportForm(forms.ModelForm):
    # market=forms.ModelChoiceField(queryset=MarketCenter.objects.all(),widget=forms.Select(attrs={'class':'js-example-basic-single','id':'market_id'}))
    primary_society = forms.ModelChoiceField(
        queryset=Association.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "society_id"}
        ),
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "year_id"}
        ),
    )
    # sale_no=forms.CharField(required=True,label='Sale no',widget=forms.TextInput(attrs={'class':'saleno_id'}))
    nill = forms.CharField(required=False)

    no = forms.CharField(required=False)

    class Meta:
        model = market_models.Pcn
        fields = ("nill",)

class AllSocietyBuyingReport(forms.ModelForm):
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "year_id"}
        ),
    )
    nill=forms.CharField(required=False)
    class Meta:
        model=market_models.Pcn
        fields=('nill',)

class RegionalPaidReportForm(forms.ModelForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "region_id"}
        ),
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "year_id"}
        ),
    )
    nill = forms.CharField(required=False)

    no = forms.CharField(required=False)

    class Meta:
        model = market_models.Pcn
        fields = ("nill",)

class VerifiedBuyingReportAll(forms.ModelForm):
    nill=forms.CharField(required=False)
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "year_id"}
        ), )
    class Meta:
        model = market_models.Pcn
        fields = ("nill",)

class VerifiedBuyingReportPerBuyer(forms.ModelForm):
    nill=forms.CharField(required=False)
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "year_id"}
        ), )
    buyer = forms.ModelChoiceField(
        queryset=market_models.Buyer.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "buyer_id"}
        ), )
    class Meta:
        model = market_models.Pcn
        fields = ("nill",)

class RegionalAnalysiForm(forms.ModelForm):
    region = forms.ModelChoiceField( required=False,
        queryset=Region.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "region_id"}
        ),
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        widget=forms.Select(
            attrs={"class": "js-example-basic-single", "id": "year_id"}
        ),
    )
    nill = forms.CharField(required=False)

    no = forms.CharField(required=False)

    class Meta:
        model = market_models.Pcn
        fields = ("nill",)
