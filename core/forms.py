from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models
from customer import models as customermodels

class ContactForm(forms.ModelForm):
    class Meta:
        model = models.contact
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'mobile', 'profile_pic']

class AssignVendorsForm(forms.ModelForm):
    class Meta:
        model = models.assign_vendor
        exclude = ['booking', 'datetime']

class VendorBidsForm(forms.ModelForm):
    class Meta:
        model = models.vendorbids
        exclude = ['booking', 'vendor', 'datetime']




class ForgotPasswordForm(forms.Form):
    mobile = forms.CharField(label='Mobile Number')

class ResetPasswordForm(forms.Form):
    otp = forms.CharField(max_length=4, label='Enter OTP')
    password1 = forms.CharField()
    password2 = forms.CharField()
    widgets = {
        'password1': forms.PasswordInput(),
        'password2': forms.PasswordInput(),
    }
