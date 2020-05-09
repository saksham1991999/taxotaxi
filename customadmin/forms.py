from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models
from core import models as coremodels

class AssignVendors(forms.ModelForm):
    class Meta:
        model = coremodels.assign_vendor
        exclude = ['booking', 'datetime']