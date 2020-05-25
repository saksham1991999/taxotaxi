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

from core import models as coremodels
from core import forms as coreforms



@login_required(login_url='/login/')
def DashboardView(request):
    try:
        customerprofile = models.customerprofile.objects.get(user = request.user)
    except:
        customerprofile = None

    if request.method == 'POST':
        type = request.POST['type']
        print(request.POST)
        if type == 'profile':


            form = forms.CustomerProfileForm(request.POST, request.FILES, instance=customerprofile)
            userform = coreforms.UserProfileForm(request.POST, request.FILES, instance=request.user)

            if form.is_valid() and userform.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()

                userform.save()
                messages.success(request, 'Details Saved Successfully',  extra_tags='alert alert-success alert-dismissible')
                return redirect('customer:dashboard')

            return redirect('customer:dashboard')

        elif type == 'change_password':
            password = request.POST['current_password']
            new_password = request.POST['new_password']
            user = authenticate(username = request.user.username, password = password)
            if user is not None:
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request, 'Password Updated',  extra_tags='alert alert-success alert-dismissible')
                return redirect('customer:dashboard')
            else:
                messages.error(request, 'Invalid Password',  extra_tags='alert alert-error alert-dismissible')
                return redirect('customer:dashboard')

        return redirect('customer:dashboard')


    else:
        payments = coremodels.payment.objects.filter(booking__user=request.user)

        upcoming_rides = coremodels.ride_booking.objects.filter(user=request.user, ride_status='Booked')
        cancelled_rides = coremodels.ride_booking.objects.filter(user=request.user, ride_status='Cancelled')
        completed_rides = coremodels.ride_booking.objects.filter(user=request.user, ride_status='Completed')

        try:
            referral_code = models.customer_promotional.objects.filter(customer__user=request.user, is_activated=True)[0]
        except:
            referral_code = None

        user = coremodels.User.objects.get(username = request.user.username)
        userform = coreforms.UserProfileForm(instance = user)
        profileform = forms.CustomerProfileForm(instance=customerprofile)
        context = {
            'profileform':profileform,
            'userform':userform,
            'referral_code':referral_code,

            'upcoming_rides':upcoming_rides,
            'cancelled_rides':cancelled_rides,
            'completed_rides':completed_rides,
        }
        return render(request, 'Customer Dashboard/customer_dashboard.html', context)


'''

@login_required(login_url='/login/')
def RegistrationView(request):
    if request.method == 'POST':
        form = forms.CustomerProfileForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user  =request.user
            new_form.save()
            return redirect('customer:dashboard')
        return redirect('customer:dashboard')
    else:
        form = forms.CustomerProfileForm()
        context = {
            'form':form,
        }
        return render(request, 'vendor_form.html' ,context)
'''