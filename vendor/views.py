from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from . import models, forms
from core import models as coremodels
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
# Create your views here.


@login_required(login_url='/login/')
def DashboardView(request):
    try:
        vendorprofile = models.vendorprofile.objects.get(user = request.user, verified=True)

        if request.method == 'POST':
            type = request.POST['type']
            print(request.POST)
            if type == 'profile':
                form = forms.VendorProfileForm(request.POST, request.FILES, instance=customerprofile)
                userform = coreforms.UserProfileForm(request.POST, request.FILES, instance=request.user)

                if form.is_valid() and userform.is_valid():
                    new_form = form.save(commit=False)
                    new_form.user = request.user
                    new_form.save()

                    userform.save()
                    messages.success(request, 'Details Saved Successfully',
                                     extra_tags='alert alert-success alert-dismissible')
                    return redirect('customer:dashboard')
                return redirect('customer:dashboard')

            elif type == 'change_password':
                password = request.POST['current_password']
                new_password = request.POST['new_password']
                user = authenticate(username=request.user.username, password=password)
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Password Updated', extra_tags='alert alert-success alert-dismissible')
                    return redirect('customer:dashboard')
                else:
                    messages.error(request, 'Invalid Password', extra_tags='alert alert-error alert-dismissible')
                    return redirect('customer:dashboard')
            return redirect('customer:dashboard')
        else:

            profileform = forms.VendorProfileForm(instance=vendorprofile)

            context = {


                'profileform':profileform,
            }
            return render(request, 'Vendor/profile.html', context)
    except:
        return redirect('core:dashboard')



def VendorRegistrationView(request):
    if request.method == 'POST':
        profile_form = forms.VendorProfileForm(request.POST, request.FILES, prefix = 'vendor')
        car_form = forms.AddCarForm(request.POST, request.FILES,prefix = 'car')
        driver_form = forms.AddDriverForm(request.POST, request.FILES,prefix = 'driver')
        bank_form = forms.BankAccountForm(request.POST, request.FILES,prefix = 'bank')

        if profile_form.is_valid() and bank_form.is_valid() and car_form.is_valid() and driver_form.is_valid():
            new_profile_form = profile_form.save(commit=False)
            vendor_mobile = profile_form.get_cleaned_data('contact1')
            vendor_email = profile_form.get_cleaned_data('email')
            vendor_fullname = profile_form.get_cleaned_data('full_name')
            vendor_password = str(vendor_fullname[:4]) + str(vendor_mobile[-4:])
            vendor = coremodels.User.objects.create_user(username=vendor_mobile, email = vendor_email, password = vendor_password)
            vendor.mobile = vendor_mobile
            vendor.is_vendor = True
            vendor.save()
            new_profile_form.user = vendor
            new_profile_form.save()

            bank_account = bank_form.save(commit=False)
            bank_account.vendor = new_profile_form
            bank_account.save()

            new_driver_form = driver_form.save(commit=False)
            new_driver_form.vendor = profile_form
            driver_mobile = new_driver_form.get_cleaned_data('contact1')
            driver_email = new_driver_form.get_cleaned_data('email')
            driver_fullname = new_driver_form.get_cleaned_data('full_name')
            driver_password = str(driver_fullname[:4]) + str(driver_mobile[-4:])
            driver = coremodels.User.objects.create_user(username=driver_mobile, email = driver_email, password = driver_password)
            driver.is_driver = True
            driver.save()
            new_driver_form.user = driver
            new_driver_form.save()


            car = car_form.save(commit=False)
            car.vendor = profile_form
            car.save()

            return redirect('core:home')
        print('--------------------------------')
        print('--------------------------------')
        print('--------------------------------')
        print(request.POST)
        print(profile_form.errors)
        print(bank_form.errors)
        print(car_form.errors)
        print(driver_form.errors)
        print(profile_form.non_field_errors())
        print(bank_form.non_field_errors())
        print(car_form.non_field_errors())
        print(driver_form.non_field_errors())
        context = {
            'profile_form':profile_form,
            'car_form':car_form,
            'driver_form':driver_form,
            'bank_form':bank_form,
        }
        return render(request, 'Vendor/registration_form.html', context)
    else:
        profile_form = forms.VendorProfileForm(prefix = 'vendor')
        car_form = forms.AddCarForm(prefix = 'car')
        driver_form = forms.AddDriverForm(prefix = 'driver')
        bank_form = forms.BankAccountForm(prefix = 'bank')
        context = {
            'profile_form':profile_form,
            'car_form':car_form,
            'driver_form':driver_form,
            'bank_form':bank_form,
        }
        return render(request, 'Vendor/registration_form.html', context)


def CarsView(request):
    if request.user.is_vendor:
        vendor = get_object_or_404(models.vendorprofile, user = request.user)
        if request.method == 'POST':
            car_form = forms.AddCarForm(request.POST, request.FILES, prefix='car')
            if car_form.is_valid():
                new_car_form = driver_form.save(commit=False)
                new_car_form.vendor = vendor
                new_car_form.save()
                return redirect('vendor:drivers')
        cars = models.vendor_cars.objects.filter(vendor = vendor)
        car_form = forms.AddCarForm(prefix='car')
        context = {
            'cars':cars,
            'car_form':car_form,
        }
        return render(request,'Vendor/cars.html', context)
    else:
        return redirect('core:dashboard')


def DriversView(request):
    if request.user.is_vendor:
        vendor = get_object_or_404(models.vendorprofile, user=request.user)
        if request.method == 'POST':
            driver_form = forms.AddDriverForm(request.POST, request.FILES, prefix='driver')
            if driver_form.is_valid():
                new_driver_form = driver_form.save(commit=False)
                new_driver_form.vendor = vendor
                new_driver_form.save()
                return redirect('vendor:drivers')
        drivers = models.vendor_cars.objects.filter(vendor = vendor)
        driver_form = forms.AddDriverForm(prefix='driver')
        context = {
            'drivers':drivers,
            'driver_form':driver_form,
        }
        return render(request,'Vendor/drivers.html', context)
    else:
        return redirect('core:dashobard')



def PaymentsView(request):
    context = {}
    return render(request,'Vendor/payments.html' , context)


def BookingsHistoryView(request):
    context = {}
    return render(request, 'Vendor/booking_history.html', context)


def BookingsView(request):
    context = {}
    return render(request, 'Vendor/bookings.html', context)


def AssignmentsView(request):
    context = {}
    return render(request, 'Vendor/assignments.html', context)


def RideDetailsView(request, id):
    context = {}
    return render(request, 'Vendor/ride_detail.html', context)


