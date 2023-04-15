from django import forms
from .models import *


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["full_name", "phone_number", "role"]

class UserForm(forms.ModelForm):
    full_name=forms.CharField(label='Full name',required=True)
    phone_number = forms.CharField(label='First Mobile number', required=True)
    role=forms.ModelChoiceField(queryset=Role.objects.all())
    class Meta:
        model = User
        fields = ["is_active", "is_staff", "is_superuser",'email','username','full_name','role','phone_number']


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["role_name"]


class PasswordForm(forms.ModelForm):
    class Meta:
        model = DefaultPassword
        fields = ["password"]
