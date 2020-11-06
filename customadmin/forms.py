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

# General
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

# Customer Forms
class CustomerForm(forms.ModelForm):
    class Meta:
        model = customermodels.customerprofile
        exclude = ['user']

class UserForm(forms.ModelForm):
    class Meta:
        model = coremodels.User
        fields = ['first_name', 'last_name', 'email', 'mobile', 'username']

# Vendor Forms
class VendorForm(forms.ModelForm):
    class Meta:
        model = vendormodels.vendorprofile
        exclude = ['user', 'total_compact', 'total_sedan', 'total_suv']

class VendorCarForm(forms.ModelForm):
    class Meta:
        model = vendormodels.vendor_cars
        exclude = ['vendor']

class VendorDriverForm(forms.ModelForm):
    class Meta:
        model = vendormodels.driver
        exclude = ['vendor', 'user']

# Popular Destinations Form
class PopularDestinationsForm(forms.ModelForm):
    class Meta:
        model = coremodels.popular_destinations
        fields = '__all__'



class FinalRideForm(forms.ModelForm):
    class Meta:
        model = coremodels.final_ride_detail
        fields = ['car', 'driver','initial_odometer_reading', 'final_odometer_reading', 'other_charges', 'collected_amount']

class AssignDriverCar(forms.ModelForm):
    class Meta:
        model = coremodels.final_ride_detail
        fields = ['car', 'driver']