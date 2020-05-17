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


def BlogsView(request):
    categories = blogmodels.categories.objects.all()


    context = {
        'categories':categories,
    }
    return render(request, 'custom_admin/blog/index.html', context)

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
