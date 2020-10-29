from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.forms import modelformset_factory, inlineformset_factory

import datetime
from . import models, forms
from vendor import models as vendormodels
from core import models as coremodels

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

def SMS(mobile, message):
    mobile = '91' + str(mobile)
    message = str(message)
    url = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=fsdCr1FyckqYrndE63halg&senderid=SMSTST&channel=2&DCS=0&flashsms=0&number='+mobile+'&text='+message+'&route=1'
    print(url)
    r = requests.post(url = url)
    x = r.text
    print(x)

@login_required(login_url='/login/')
def DashboardView(request):
    # try:
        driver_profile = get_object_or_404(vendormodels.driver, user = request.user)

        if request.method == 'POST':
            type = request.POST['type']
            if type == 'profile':
                profile_form = forms.DriverProfileForm(request.POST, request.FILES, instance=driver_profile)
                if profile_form.is_valid():
                    profile_form.save()
                    messages.success(request, 'Details Saved Successfully',
                                     extra_tags='alert alert-success alert-dismissible')
                    return redirect('driver:dashboard')
                else:
                    messages.success(request, 'Please Update Details Correctly',
                                     extra_tags='alert alert-danger alert-dismissible')
                    context = {
                        'profile_form': profile_form,
                        'driver': driver_profile,
                    }
                    return render(request, 'Driver/profile.html', context)
            elif type == 'change_password':
                password = request.POST['current_password']
                new_password = request.POST['new_password']
                user = authenticate(username=request.user.username, password=password)
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Password Updated', extra_tags='alert alert-success alert-dismissible')
                    return redirect('driver:dashboard')
                else:
                    messages.error(request, 'Invalid Password', extra_tags='alert alert-error alert-dismissible')
        else:
            profile_form = forms.DriverProfileForm(instance=driver_profile)

            context = {
                'profile_form':profile_form,
                'driver':driver_profile,
            }
            print("#--------------------------------------------------------------------------#")
            return render(request, 'Driver/profile.html', context)
    # except:
    #     print("WHY")
    #     return redirect('core:dashboard')

def UpcomingRidesView(request):
    driver = vendormodels.driver.objects.get(user=request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(driver = driver).filter(booking__ride_status__in = ["Assigned Car/Driver"] )
    form = forms.FinalRideForm()
    context = {
        'final_rides':final_rides,
        'form':form,
    }
    return render(request, 'Driver/ride_detail.html', context)

def RideDetailsView(request):
    driver = vendormodels.driver.objects.get(user=request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(driver = driver).filter(booking__ride_status__in = ["Ongoing"] )
    form = forms.FinalRideForm()
    context = {
        'final_rides':final_rides,
        'form':form,
    }
    return render(request, 'Driver/ride_detail.html', context)

def StartRideView(request, id):
    if request.method == "POST":
        final_ride = get_object_or_404(coremodels.final_ride_detail, id=id)
        form = forms.FinalRideForm(request.POST, instance = final_ride )
        if form.is_valid():
            form.save()
            final_ride.start_datetime = datetime.datetime.now()
            booking = final_ride.booking
            booking.ride_status = "Ongoing"
            final_ride.save()
            booking.save()
            messages.success(
                request,
                'Ride Started',
                extra_tags='alert alert-success alert-dismissible'
            )
            return redirect('driver:booking_detail')
        else:
            print(form.errors)
            messages.error(
                request,
                'Please Fill Details Correctly',
                extra_tags='alert alert-danger alert-dismissible'
            )
            return redirect('driver:booking_detail')

def EndRideView(request, id):
    if request.method == "POST":
        final_ride = get_object_or_404(coremodels.final_ride_detail, id=id)
        form = forms.FinalRideForm(instance = final_ride)
        if form.is_valid():
            form.save()
            final_ride.end_datetime = datetime.datetime.now()
            booking = final_ride.booking
            booking.ride_status = "Completed"
            final_ride.save()
            booking.save()
            messages.success(
                request,
                'Ride Ended',
                extra_tags='alert alert-success alert-dismissible'
            )
            return redirect('driver:booking_detail')
        else:
            messages.error(
                request,
                'Please Fill Details Correctly',
                extra_tags='alert alert-danger alert-dismissible'
            )
            return redirect('driver:booking_detail')

def RejectBookingView(request, id):
    if request.method == "POST":

        final_ride = get_object_or_404(coremodels.final_ride_detail, id=id)

        rejection_reason = request.POST['rejection_reason']
        bid = final_ride.bid
        bid.rejection_reason = rejection_reason
        bid.save()

        booking = final_ride.booking
        booking.ride_status = "Booked"
        booking.save()

        booking.assign_vendor.delete()
        final_ride.delete()

        messages.success(
            request,
            'Assignment Rejected',
            extra_tags='alert alert-success alert-dismissible'
        )
        return redirect('driver:assignments')

def BookingsHistoryView(request):
    driver = vendormodels.driver.objects.get(user= request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(driver = driver, booking__ride_status = "Verified")
    # final_rides = coremodels.final_ride_detail.objects.all()
    context = {
        'final_rides':final_rides
    }
    return render(request, 'Driver/booking_history.html', context)

def PaymentsView(request):
    driver = vendormodels.driver.objects.get(user= request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(driver = driver, booking__ride_status="Verified")
    context = {
        'final_rides': final_rides
    }
    return render(request,'Driver/payments.html' , context)














def BookingsView(request):
    driver = vendormodels.driver.objects.get(user= request.user)
    bookings = coremodels.ride_booking.objects.filter(ride_status = "Selected Vendors", final_ride__driver = driver)

    if "sort" in request.GET:
        sort = request.GET["sort"]
        if sort.lower() == "date":
            bookings = bookings.order_by('-pickup_datetime')
        else:
            bookings = bookings.order_by('id')


    context = {
        "bookings":bookings,
    }
    return render(request, 'Driver/bookings.html', context)


def AssignmentsView(request):
    vendor = models.vendorprofile.objects.get(user=request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(bid__vendor = vendor).filter(booking__ride_status = "Assigned Vendor" )
    context = {
        'final_rides':final_rides
    }
    return render(request, 'Vendor/assignments.html', context)






