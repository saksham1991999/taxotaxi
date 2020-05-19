from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import requests, datetime
from django.contrib.auth import authenticate, login, logout

from . import models, forms
from core import models as coremodels
from blog import models as blogmodels
from customer import models as customermodels
from vendor import models as vendormodels


def HomeView(request):
    context = {}
    return render(request, 'custom_admin/index.html',context)

def TestView1(request):
    context = {}
    return render(request, 'test/1.html',context)


def TestView2(request):
    context = {}
    return render(request, 'test/2.html',context)


def TestView3(request):
    context = {}
    return render(request, 'test/3.html',context)


def TestView4(request):
    context = {}
    return render(request, 'test/4.html',context)


def TestView5(request):
    context = {}
    return render(request, 'test/5.html',context)

# Ride Bookings View


# MAIN PAGE VIEWS
def GeneralModelsView(request):

    context = {}
    return render(request, 'general/index.html', context)

def AddCityView(request):
    context = {}
    return render(request, 'general/city_form.html', context)

def EditCityView(request):
    context = {}
    return render(request, 'general/city_form.html', context)

def DeleteCityView(request):
    context = {}
    return render(request, 'custom_admin/general/index.html', context)

def AddTestimonialView(request):
    context = {}
    return render(request, 'general/testimonial_form.html', context)

def EditTestimonialView(request, id):
    context = {}
    return render(request, 'general/testimonial_form.html', context)

def DeleteTestimonialView(request, id):
    context = {}
    return render(request, 'custom_admin/general/index.html', context)

def AddMainPageBannersView(request):
    context = {}
    return render(request, 'general/banners_form.html', context)

def EditMainPageBannersView(request, id):
    context = {}
    return render(request, 'general/banners_form.html', context)

def DeleteMainPageBannersView(request, id):
    context = {}
    return render(request, 'custom_admin/general/index.html', context)

def UpdateFAQsView(request):
    context = {}
    return render(request, 'general/faqs_formset.html', context)

def ContactUsView(request):
    context = {}
    return render(request, 'general/contact_us.html', context)


# CAR SELECTION PAGE VIEWS
def CarTypePageViews(request):
    context = {}
    return render(request, 'car_type/index.html', context)

def UpdateCarAttributes(request):
    context = {}
    return render(request, 'car_type/car_attribute_formset.html', context)

def UpdateCarAttributeValueView(request, id):
    context = {}
    return render(request, 'car_type/car_attribute_value_form.html', context)

def UpdateRideAdditionalChoices(request):
    context = {}
    return render(request, 'car_type/additional_choices_formset.html', context)

def UpdateCityRideAttributeValues(request, id):
    context = {}
    return render(request, 'car_type/city_ride_attributes_form.html', context)


# Popular Destinations View
def PopularDestinationsView(request):
    context = {}
    return render(request, 'custom_admin/popular_destinations/index.html', context)

def AddPopularDestinationView(request):
    context = {}
    return render(request, 'custom_admin/popular_destinations/index.html', context)

def EditPopularDestinationView(request):
    context = {}
    return render(request, 'custom_admin/popular_destinations/index.html', context)

def DeletePopularDestinationView(request):
    context = {}
    return render(request, 'custom_admin/popular_destinations/index.html', context)


# BLOG VIEWS
def BlogsView(request):
    categories = blogmodels.categories.objects.all()
    context = {
        'categories':categories,
    }
    return render(request, 'blogs/index.html', context)

def UpdateBlogCategoriesView(request):

    context = {}
    return render(request, 'blogs/categories_formset.html', context)

def AddBlogPostView(request):

    if request.method == 'POST':
        pass
    else:
        form = forms.BlogPostForm()
        context = {
            'form':form,
        }
        return render(request, 'blogs/blog_form.html', context)

def EditBlogPostView(request, id):
    context = {}
    return render(request, 'custom_admin/blog/index.html', context)

def DeleteBlogPostView(request, id):

    return redirect('')


# CUSTOMER VIEWS
def CustomersView(request):

    customers = customermodels.customerprofile.objects.all()

    context = {
        'customers':customers,
    }
    return render(request, 'customers/index.html', context)

def AddCustomerView(request):
    if request.method == 'POST':
        pass
    else:
        userform = forms.UserForm()
        profileform = forms.CustomerForm()
        context = {
            'profileform':profileform,
            'userform':userform,
        }
        return render(request, 'customers/customer_form.html', context)

def EditCustomerView(request, id):
    context = {}
    return render(request, 'customers/customer_form.html', context)

def DeleteCustomerView(request, id):
    context = {}
    return render(request, 'customers/', context)

def UpdateCustomerPromotionalView(request, id):
    context = {}
    return render(request, 'customers/promotionals_formset.html', context)


# Vendor Views
def VendorsView(request):
    context = {}
    return render(request, 'vendors/index.html', context)

def VendorView(request):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def AddVendorView(request):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def EditVendorView(request):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def DeleteVendorView(request):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def AddVendorCarView(request, id):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def EditVendorCarView(request, id):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def DeleteVendorCarView(request, id):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def AddVendorDriver(request):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def EditVendorDriver(request, id):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)

def DeleteVendorDriver(request, id):
    context = {}
    return render(request, 'custom_admin/customers/index.html', context)






def DashboardView(request):
    assign_vendors = coremodels.booking.objects.filter(advance_payment_received=True, assigned_vendors=False)
    assign_final_vendors = coremodels.booking.objects.filter(advance_payment_received=True, assigned_vendors=True, assign_final_vendors=False)
    completed_rides = coremodels.booking.objects.filter(ride_status='Co')
    payments = coremodels.payment.objects.all()
    context = {
        'assign_vendors':assign_vendors,
        'assign_final_vendors':assign_final_vendors,
        'completed_rides':completed_rides,
        'payments':payments,
    }
    return render(request, '', context)

def AssignVendorsView(request, id):
    if request.method == 'POST':
        form = forms.AssignVendors(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            booking = coremodels.ride_booking.objects.get(booking_id=id)
            new_form.booking = booking
            new_form.datetime = datetime.datetime.now()
            new_form.save()
            for vendor in new_form.vendors:
                vendorbid = coremodels.vendorbids.objects.create(booking=booking)
                vendorbid.max_bid = booking.ride_fare*(1-(new_form.commission/100))
                vendorbid.save()
        return redirect('custom_admin:dashboard')
    else:
        form = forms.AssignVendors()
        context = {
            'form':form,
        }
        return render(request, '', context)

def VendorBidsView():
    pass

def AssignFinalVendorView(request, id):
    pass
