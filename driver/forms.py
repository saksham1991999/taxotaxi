from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models
from vendor import models as vendormodels
from core import models as coremodels



class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = vendormodels.driver
        exclude = ['vendor', 'status']

    # def clean_contact1(self):
    #     mobile = self.cleaned_data.get('contact1')
    #     if mobile:
    #         try:
    #             user = coremodels.User.objects.get(username = mobile)
    #             raise forms.ValidationError('Mobile Number is already registered')
    #         except:
    #             return mobile


class FinalRideForm(forms.ModelForm):
    class Meta:
        model = coremodels.final_ride_detail
        fields = ['initial_odometer_reading', 'final_odometer_reading', 'other_charges', 'collected_amount']
