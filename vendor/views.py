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
from core import models as coremodels
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
# Create your views here.
def SMS(mobile, message):
    mobile = '91' + str(mobile)
    message = str(message)
    url = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=fsdCr1FyckqYrndE63halg&senderid=TAXOTR&channel=2&DCS=0&flashsms=0&number='+mobile+'&text='+message+'&route=1'
    print(url)
    r = requests.post(url = url)
    x = r.text
    print(x)

def VendorRegistrationView(request):
    if request.method == 'POST':
        profile_form = forms.VendorProfileForm(request.POST, request.FILES, prefix = 'vendor')
        car_form = forms.AddCarForm(request.POST, request.FILES,prefix = 'car')
        driver_form = forms.AddDriverForm(request.POST, request.FILES,prefix = 'driver')
        bank_form = forms.BankAccountForm(request.POST, request.FILES,prefix = 'bank')

        if profile_form.is_valid() and bank_form.is_valid() and car_form.is_valid() and driver_form.is_valid():
            new_profile_form = profile_form.save(commit=False)
            vendor_mobile = profile_form.cleaned_data['contact1']
            vendor_email = profile_form.cleaned_data['email']
            vendor_fullname = profile_form.cleaned_data['full_name']
            vendor_password = str(vendor_fullname[:4]) + str(vendor_mobile[-4:])
            vendor = coremodels.User.objects.create_user(username=vendor_mobile, email = vendor_email, password = vendor_password)
            vendor.mobile = vendor_mobile
            vendor.is_vendor = True
            vendor.save()
            new_profile_form.status = "Hold"
            new_profile_form.user = vendor
            new_profile_form.save()

            referal_code = coremodels.user_referral.objects.create(user=vendor, promotional_code=str(vendor_mobile),
                                                               referralbenefit=50,
                                                               customerbenefit=50, is_activated=True)
            text = 'Thank you for submitting details. We”ll get back to you soon.'
            SMS(vendor_mobile, text)

            bank_account = bank_form.save(commit=False)
            bank_account.vendor = new_profile_form
            bank_account.save()

            new_driver_form = driver_form.save(commit=False)
            new_driver_form.vendor = new_profile_form
            driver_mobile = driver_form.cleaned_data['contact1']
            driver_email = driver_form.cleaned_data['email']
            driver_fullname = driver_form.cleaned_data['full_name']
            driver_password = str(driver_fullname[:4]) + str(driver_mobile[-4:])

            # year instead of Full Name
            if 'same' in request.POST:
                driver = vendor
            else:
                driver = coremodels.User.objects.create_user(username=driver_mobile, email = driver_email, password = driver_password)
                driver.is_driver = True
                driver.save()
                referal_code = coremodels.user_referral.objects.create(user=driver, promotional_code=str(driver_mobile),
                                                                       referralbenefit=50,
                                                                       customerbenefit=50, is_activated=True)
            new_driver_form.status = "Hold"
            new_driver_form.user = driver
            new_driver_form.save()

            text = 'Thanks for registering on TaxoTaxi, We will verify and contact you soon!'
            SMS(driver_mobile, text)
            car = car_form.save(commit=False)
            car.status = "Hold"
            car.vendor = new_profile_form
            car.save()
            messages.success(request, 'Details Submitted Successfully. Please wait till the confirmation is received.',
                             extra_tags='alert alert-success alert-dismissible')
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
        messages.error(request, 'Please fill the form correctly',
                         extra_tags='alert alert-danger alert-dismissible')
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


@login_required(login_url='/login/')
def DashboardView(request):
    try:
        vendorprofile = get_object_or_404(models.vendorprofile, user = request.user)
        VendorBankFormset = inlineformset_factory(models.vendorprofile,
                                                           models.bank_detail, exclude=['vendor'],
                                                           extra=0, can_delete=False)
        if request.method == 'POST':
            type = request.POST['type']
            if type == 'profile':
                profile_form = forms.VendorProfileForm(request.POST, request.FILES, instance=vendorprofile)
                bank_formset = VendorBankFormset(request.POST, request.FILES, instance = vendorprofile)
                if profile_form.is_valid() and bank_formset.is_valid():
                    profile_form.save()
                    bank_formset.save()
                    messages.success(request, 'Details Saved Successfully',
                                     extra_tags='alert alert-success alert-dismissible')
                    return redirect('vendor:dashboard')
                else:
                    messages.success(request, 'Please Update Details Correctly',
                                     extra_tags='alert alert-danger alert-dismissible')
                    context = {
                        'profile_form': profile_form,
                        'bank_formset': bank_formset,
                        'vendor': vendorprofile,
                    }
                    return render(request, 'Vendor/profile.html', context)
            elif type == 'change_password':
                password = request.POST['current_password']
                new_password = request.POST['new_password']
                user = authenticate(username=request.user.username, password=password)
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Password Updated', extra_tags='alert alert-success alert-dismissible')
                    return redirect('vendor:dashboard')
                else:
                    messages.error(request, 'Invalid Password', extra_tags='alert alert-error alert-dismissible')
        else:
            profile_form = forms.VendorProfileForm(instance=vendorprofile)
            bank_formset = VendorBankFormset(instance = vendorprofile)
            context = {
                'profile_form':profile_form,
                'bank_formset':bank_formset,
                'vendor':vendorprofile,
            }
            return render(request, 'Vendor/profile.html', context)
    except:
        return redirect('core:dashboard')


def CarsView(request):
    if request.user.is_vendor:
        vendor = get_object_or_404(models.vendorprofile, user = request.user)
        if request.method == 'POST':
            car_form = forms.AddCarForm(request.POST, request.FILES, prefix='car')
            if car_form.is_valid():
                new_car_form = car_form.save(commit=False)
                new_car_form.vendor = vendor
                new_car_form.status = 'Pending'
                new_car_form.save()
                return redirect('vendor:cars')
            cars = models.vendor_cars.objects.filter(vendor=vendor)
            context = {
                'cars': cars,
                'car_form': car_form,
            }
            return render(request, 'Vendor/cars.html', context)
        else:
            cars = models.vendor_cars.objects.filter(vendor = vendor)
            car_form = forms.AddCarForm(prefix='car')
            context = {
                'cars':cars,
                'car_form':car_form,
            }
            return render(request,'Vendor/cars.html', context)
    else:
        return redirect('core:dashboard')

def EditCarView(request, id):
    if request.user.is_vendor:
        vendor = get_object_or_404(models.vendorprofile, user = request.user)
        car = get_object_or_404(models.vendor_cars, id = id)
        if request.method == 'POST':
            car_form = forms.AddCarForm(request.POST, request.FILES, prefix='car', instance=car)
            if car_form.is_valid() and car.vendor == vendor:
                new_car_form = car_form.save(commit=False)
                new_car_form.save()
                return redirect('vendor:cars')
            context = {
                'car_form': car_form,
            }
            return render(request,'Vendor/edit-car.html', context)
        else:
            car_form = forms.AddCarForm(prefix='car', instance=car)
            context = {
                'car_form':car_form,
            }
            return render(request,'Vendor/edit-car.html', context)
    else:
        return redirect('core:dashboard')

def DeleteCarView(request, id):
    if request.user.is_vendor and request.user.is_authenticated:
        vendor = get_object_or_404(models.vendorprofile, user = request.user)
        car = get_object_or_404(models.vendor_cars, id = id)
        if car.vendor == vendor:
            car.delete()
        return redirect('vendor:cars')
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
                driver_mobile = driver_form.cleaned_data['contact1']
                driver_email = driver_form.cleaned_data['email']
                driver_fullname = driver_form.cleaned_data['full_name']
                driver_password = str(driver_fullname[:4]) + str(driver_mobile[-4:])
                driver = coremodels.User.objects.create_user(username=driver_mobile, email=driver_email,
                                                             password=driver_password)
                driver.is_driver = True
                driver.save()
                new_driver_form.status = "Hold"
                new_driver_form.user = driver
                new_driver_form.save()
                return redirect('vendor:drivers')
            drivers = models.driver.objects.filter(vendor=vendor)
            context = {
                'drivers': drivers,
                'driver_form': driver_form,
            }
            return render(request, 'Vendor/drivers.html', context)
        else:
            drivers = models.driver.objects.filter(vendor = vendor)
            driver_form = forms.AddDriverForm(prefix='driver')
            context = {
                'drivers':drivers,
                'driver_form':driver_form,
            }
            return render(request,'Vendor/drivers.html', context)
    else:
        return redirect('core:dashobard')

def EditDriverView(request, id):
    if request.user.is_vendor:
        vendor = get_object_or_404(models.vendorprofile, user=request.user)
        driver = get_object_or_404(models.driver, id = id)
        if request.method == 'POST':
            driver_form = forms.AddDriverForm(request.POST, request.FILES, prefix='driver', instance=driver)
            if driver_form.is_valid() and driver.vendor == vendor:
                driver_form.save()
                return redirect('vendor:drivers')
            context = {
                'driver_form': driver_form,
            }
            return render(request, 'Vendor/edit-driver.html', context)
        else:
            driver_form = forms.AddDriverForm(prefix='driver', instance=driver)
            context = {
                'driver_form':driver_form,
            }
            return render(request,'Vendor/edit-driver.html', context)
    else:
        return redirect('core:dashobard')

def DeleteDriverView(request, id):
    if request.user.is_vendor:
        vendor = get_object_or_404(models.vendorprofile, user=request.user)
        driver = get_object_or_404(models.driver, id = id)
        if driver.vendor == vendor:
            driver.delete()
        return redirect('vendor:drivers')
    else:
        return redirect('core:dashobard')

def PaymentsView(request):
    vendor = models.vendorprofile.objects.get(user=request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(bid__vendor=vendor, booking__ride_status="Verified")
    context = {
        'final_rides': final_rides
    }
    return render(request,'Vendor/payments.html' , context)



def BookingsView(request):
    vendor = models.vendorprofile.objects.get(user= request.user)
    bookings = coremodels.ride_booking.objects.filter(ride_status = "Selected Vendors", assign_vendor__vendors__in = [vendor])
    # query = coremodels.assign_vendor.objects.filter(booking__ride_status = "Selected Vendors", vendors__in = [vendor])

    if "sort" in request.GET:
        sort = request.GET["sort"]
        if sort.lower() == "date":
            bookings = bookings.order_by('-pickup_datetime')
        else:
            bookings = bookings.order_by('id')

    if "your-bookings" in request.GET:
        bookings_id = coremodels.vendorbids.objects.filter(vendor = vendor).values('booking').distinct()
        bookings = coremodels.ride_booking.objects.filter(id__in = bookings_id)
        bookings = bookings.filter(ride_status = "Selected Vendors", assign_vendor__vendors__in = [vendor])

    context = {
        "bookings":bookings,
    }
    return render(request, 'Vendor/bookings.html', context)


def AssignmentsView(request):
    vendor = models.vendorprofile.objects.get(user=request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(bid__vendor = vendor).filter(booking__ride_status = "Assigned Vendor" )
    context = {
        'final_rides':final_rides
    }
    return render(request, 'Vendor/assignments.html', context)

def BookingsHistoryView(request):
    vendor = models.vendorprofile.objects.get(user=request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(bid__vendor = vendor, booking__ride_status = "Verified")
    # final_rides = coremodels.final_ride_detail.objects.all()
    context = {
        'final_rides':final_rides
    }
    return render(request, 'Vendor/booking_history.html', context)


def RideDetailsView(request):
    vendor = models.vendorprofile.objects.get(user=request.user)
    final_rides = coremodels.final_ride_detail.objects.filter(bid__vendor = vendor).filter(booking__ride_status__in = ["Assigned Car/Driver", "Ongoing"] )
    form = forms.FinalRideForm()
    context = {
        'final_rides':final_rides,
        'form':form,
    }
    return render(request, 'Vendor/ride_detail.html', context)

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
            return redirect('vendor:booking_detail')
        else:
            print(form.errors)
            messages.error(
                request,
                'Please Fill Details Correctly',
                extra_tags='alert alert-danger alert-dismissible'
            )
            return redirect('vendor:booking_detail')

def EndRideView(request, id):
    if request.method == "POST":
        final_ride = get_object_or_404(coremodels.final_ride_detail, id=id)
        form = forms.FinalRideForm(request.POST, instance = final_ride)
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
            return redirect('vendor:booking_detail')
        else:
            messages.error(
                request,
                'Please Fill Details Correctly',
                extra_tags='alert alert-danger alert-dismissible'
            )
            return redirect('vendor:booking_detail')

def AssignCarDriverView(request, id):
    if request.method == "POST":
        final_ride = get_object_or_404(coremodels.final_ride_detail, id=id)
        form = forms.AssignCarDriverForm(request.POST, instance = final_ride)
        if form.is_valid():
            form.save()
            booking = final_ride.booking
            booking.ride_status = "Assigned Car/Driver"
            final_ride.save()
            booking.save()
            customer_message = "We have assigned Driver Name: " + str(final_ride.driver.full_name) + " (" + str(final_ride.driver.contact1) + ") " + "and Car Number: " + str(final_ride.car.registration_no)
            SMS(str(booking.phone_no), customer_message)

            driver_message = "You have been assigned to " + str(booking.name) + " (" + str(booking.phone_no) + " ) for " + str(booking.ride_type) + " ride, on dated " + str(booking.pickup_datetime) + " from " + str(booking.pickup_city) + " to " + str(booking.drop_city)
            SMS(str(final_ride.driver.contact1), driver_message)
            messages.success(
                request,
                'Car and Driver Assigned.',
                extra_tags='alert alert-success alert-dismissible'
            )
            return redirect('vendor:assignments')
        messages.error(
            request,
            "Couldn't Assign Car and Driver",
            extra_tags='alert alert-danger alert-dismissible'
        )
        return redirect('vendor:assignments')

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
        return redirect('vendor:assignments')

def VendorBookingBidView(request):
    if request.method == "POST":
        user = int(request.POST["user_id"])
        vendor = get_object_or_404(models.vendorprofile, user__id = user)
        booking_id = int(request.POST["booking_id"])
        booking = get_object_or_404(coremodels.ride_booking, id = booking_id)
        bid = int(request.POST["bid"])
        bid_qs, created = coremodels.vendorbids.objects.get_or_create(vendor=vendor, booking=booking, bid=bid)
        bid_qs.save()
        return JsonResponse({"status": "success"}, status=200)
