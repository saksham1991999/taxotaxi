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
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from core import models as coremodels
from core import forms as coreforms
from core.payu import PAYU
payu = PAYU()


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
                messages.error(request, 'Invalid Password',  extra_tags='alert alert-danger alert-dismissible')
                return redirect('customer:dashboard')

        return redirect('customer:dashboard')


    else:
        payments = coremodels.payment.objects.filter(booking__user=request.user)

        upcoming_rides = coremodels.ride_booking.objects.filter(user=request.user).exclude(ride_status__in = ['Cancelled', 'Verified', "User Cancelled"])
        cancelled_rides = coremodels.ride_booking.objects.filter(user=request.user, ride_status='User Cancelled')
        incomplete_rides = coremodels.ride_booking.objects.filter(user=request.user, ride_status='Cancelled')
        completed_rides = coremodels.ride_booking.objects.filter(user=request.user, ride_status='Verified')

        try:
            referral_codes = coremodels.user_referral.objects.filter(user=request.user, is_activated=True)
        except:
            referral_codes = None

        user = coremodels.User.objects.get(username = request.user.username)
        userform = coreforms.UserProfileForm(instance = user)
        profileform = forms.CustomerProfileForm(instance=customerprofile)
        context = {
            'profileform':profileform,
            'userform':userform,
            'referral_codes':referral_codes,

            'upcoming_rides':upcoming_rides,
            'cancelled_rides':cancelled_rides,
            'completed_rides':completed_rides,
            'incomplete_rides':incomplete_rides,
        }
        return render(request, 'Customer Dashboard/customer_dashboard.html', context)

def CustomerFeedback(request):
    if request.method == "POST":
        final_ride_id = request.POST.get('final_ride_id')
        comment = request.POST.get('comment')
        feedback = request.POST.getlist("feedback")
        total = 6
        avg = len(feedback)/total
        final_ride = get_object_or_404(coremodels.final_ride_detail, id=final_ride_id)
        final_ride.review = comment
        final_ride.rating = avg
        final_ride.save()
        return HttpResponse({"Status": "Feedback Submitted Successfuly!"}, status = HTTP_200_OK)

def CancelRideView(request, id):
    booking = get_object_or_404(coremodels.ride_booking, id=id)
    booking.ride_status = 'User Cancelled'
    booking.save()
    return redirect('customer:dashboard')

def CompletePayment(request, id):
    booking = get_object_or_404(coremodels.ride_booking, id=id)
    data = {
        'txnid': payu.generate_txnid(), 'amount': str(int(booking.advance)), 'productinfo': str(booking.ride_type),
        'firstname': str(request.user.first_name), 'email': str(request.user.email), 'udf1': str(booking.id),
    }
    # print(data)
    payu_data = payu.initiate_transaction(data)
    print('--------------------PAYMENT VIEW Rendering ----------------------------')
    return render(request, 'payments/payu_checkout.html', {"posted": payu_data})


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