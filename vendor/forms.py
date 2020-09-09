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
        mobile = self.cleaned_data['contact1']
        user = coremodels.User.objects.filter(username=mobile)
        if user.exists():
            raise forms.ValidationError('Mobile Number is already registered')
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
        exclude = ['vendor', 'status', 'user']

    def clean_contact1(self):
        mobile = self.cleaned_data['contact1']
        user = coremodels.User.objects.filter(username=mobile)
        if user.exists():
            raise forms.ValidationError('Mobile Number is already registered')
        return mobile

class AssignCarDriverForm(forms.ModelForm):
    class Meta:
        model = coremodels.final_ride_detail
        fields = ['car', 'driver']


class FinalRideForm(forms.ModelForm):
    class Meta:
        model = coremodels.final_ride_detail
        fields = ['initial_odometer_reading', 'final_odometer_reading', 'other_charges', 'collected_amount']
