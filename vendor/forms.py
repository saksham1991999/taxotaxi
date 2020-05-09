from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = models.vendorprofile
        exclude = ['user']

class AddCarForm(forms.ModelForm):
    class Meta:
        model = models.vendor_cars
        exclude = ['vendor']

class AddDriverForm(forms.ModelForm):
    class Meta:
        model = models.driver
        exclude = ['vendor']