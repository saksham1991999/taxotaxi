from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models
from core import models as coremodels


class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = models.vendorprofile
        exclude = ['user', 'status']

    def clean_contact1(self):
        mobile = self.cleaned_data.get('contact1')
        if mobile:
            try:
                user = coremodels.User.objects.get(username = mobile)
                raise forms.ValidationError('Mobile Number is already registered')
            except:
                return mobile


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = models.bank_detail
        exclude = ['vendor', 'status']


class AddCarForm(forms.ModelForm):
    class Meta:
        model = models.vendor_cars
        exclude = ['vendor', 'status']


class AddDriverForm(forms.ModelForm):
    class Meta:
        model = models.driver
        exclude = ['vendor', 'status']