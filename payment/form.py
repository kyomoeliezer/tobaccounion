from django import forms
from .models import *

class PaymentForm(forms.ModelForm):
    amount=forms.CharField(label='Amount Paid')
    class Meta:
        model=Payment
        exclude = ('created_by','created_on','amount')
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 2, 'cols': 12}),
            'dated': forms.TextInput(attrs={'class':'datepicker','type':'date'}),
            'amount': forms.TextInput(attrs={'class': 'money', 'type': 'text'}),
        }

class PaymentFormEdit(forms.ModelForm):
    class Meta:
        model=Payment
        exclude = ('created_by','created_on')
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 2, 'cols': 12}),
            'dated': forms.TextInput(attrs={'class':'datepicker','type':'date'}),
        }

