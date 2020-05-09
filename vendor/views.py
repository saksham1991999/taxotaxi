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
            return render(request, 'vendor_dashboard.html', context)
    except:
        return redirect('vendor:registration')


@login_required(login_url='/login/')
def VendorRegistrationView(request):
    if request.method == 'POST':
        form = forms.VendorProfileForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('vendor:dashboard')
        return redirect('vendor:dashboard')
    else:
        form = forms.VendorProfileForm()
        context = {
            'form':form,
        }
        return render(request, 'vendor_form.html' ,context)
