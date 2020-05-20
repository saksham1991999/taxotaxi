from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import models
from core import models as coremodels
from vendor import models as vendormodels
from customer import models as customermodels
from blog import models as blogmodels

class AssignVendors(forms.ModelForm):
    class Meta:
        model = coremodels.assign_vendor
        exclude = ['booking', 'datetime']

class CityForm(forms.ModelForm):
    class Meta:
        model = coremodels.city
        exclude = []

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = coremodels.testimonials
        exclude = []

class BannersForm(forms.ModelForm):
    class Meta:
        model = coremodels.banner
        exclude = []

class CarAttributeValueForm(forms.ModelForm):
    class Meta:
        model = coremodels.car_attr_comparison
        exclude = []

class CityRideAttributeForm(forms.ModelForm):
    class Meta:
        model = coremodels.calc_city_attr_value
        exclude = []


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = blogmodels.post
        exclude = []


class CustomerForm(forms.ModelForm):
    class Meta:
        model = customermodels.customerprofile
        exclude = []

class UserForm(forms.ModelForm):
    class Meta:
        model = coremodels.User
        fields = ['first_name', 'last_name', 'email', 'mobile', 'username']

class VendorForm(forms.ModelForm):
    class Meta:
        model = vendormodels.vendorprofile
        exclude = []

class VendorCarForm(forms.ModelForm):
    class Meta:
        model = vendormodels.vendor_cars
        exclude = ['vendor']

class VendorDriverForm(forms.ModelForm):
    class Meta:
        model = vendormodels.driver
        exclude = ['vendor']

