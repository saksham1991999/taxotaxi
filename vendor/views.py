from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from . import models, forms
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
# Create your views here.

@login_required(login_url='/login/')
def DashboardView(request):
    try:
        vendorprofile = models.vendorprofile.objects.get(user = request.user, verified=1)
        if request.method == 'POST':
            type = request.POST['type']
            print(request.POST)
            if type == 'profile':
                form = forms.VendorProfileForm(request.POST, request.FILES, instance=vendorprofile)
                print(form.errors)
                if form.is_valid():
                    form.save()
                    return redirect('vendor:dashboard')
            elif type == 'addcar':
                form = forms.AddCarForm(request.POST, request.FILES)
                print(form.errors)
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.vendor = vendorprofile
                    new_form.save()
                    return redirect('vendor:dashboard')
            elif type == 'adddriver':
                form = forms.AddDriverForm(request.POST, request.FILES)
                print(form.errors)
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.vendor = vendorprofile
                    new_form.save()
                    return redirect('vendor:dashboard')
            return redirect('vendor:dashboard')

        else:
            cars = models.vendor_cars.objects.filter(vendor=vendorprofile)
            drivers = models.driver.objects.filter(vendor=vendorprofile)

            profileform = forms.VendorProfileForm(instance=vendorprofile)
            addcarform = forms.AddCarForm()
            adddriverform = forms.AddDriverForm()

            context = {
                'cars':cars,
                'drivers':drivers,
                'profileform':profileform,
                'addcarform':addcarform,
                'adddriverform':adddriverform,
            }
            return render(request, 'Vendor/profile.html', context)
    except:
        return redirect('vendor:registration')


def VendorRegistrationView(request):
    if request.method == 'POST':
        profile_form = forms.VendorProfileForm(request.POST, request.FILES, prefix = 'vendor')
        car_form = forms.AddCarForm(request.POST, request.FILES,prefix = 'car')
        driver_form = forms.AddDriverForm(request.POST, request.FILES,prefix = 'driver')
        bank_form = forms.BankAccountForm(request.POST, request.FILES,prefix = 'bank')

        if profile_form.is_valid() and bank_form.is_valid() and car_form.is_valid() and driver_form.is_valid():
            profile_form.save()

            bank_account = bank_form.save(commit=False)
            bank_account.vendor = profile_form
            bank_account.save()

            driver = driver_form.save(commit=False)
            driver.vendor = profile_form
            driver.save()

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
    context = {}
    return render(request,'Vendor/cars.html', context)


def DriversView(request):
    context = {}
    return render(request,'Vendor/drivers.html', context)


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


