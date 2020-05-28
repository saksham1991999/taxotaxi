from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import get_list_or_404, get_object_or_404
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
def CancelledRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(ride_status = 'Cancelled')
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/cancelled_rides.html', context)

def BookedRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(ride_status = 'Booked')
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/cancelled_rides.html', context)

def AssignVendorRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(assigned_vendors = True)
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/cancelled_rides.html', context)

def UpcomingRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(assigned_final_vendor = True)
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/cancelled_rides.html', context)

def OngoingRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(ride_status = 'Ongoing')
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/cancelled_rides.html', context)

def CompletedRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(ride_status = 'Completed')
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/cancelled_rides.html', context)

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

def VendorBidsView(request, id):
    pass

def AssignFinalVendorView(request, id):
    pass

# MAIN PAGE VIEWS
def GeneralModelsView(request):
    cities = coremodels.city.objects.all()
    testimonials = coremodels.testimonials.objects.all()
    banners = coremodels.banner.objects.all()
    faqs = coremodels.faq.objects.all()
    terms_and_conditions = coremodels.TermsAndConditions.objects.all()
    context = {
        'cities':cities,
        'testimonials':testimonials,
        'banners':banners,
        'faqs':faqs,
        'terms_and_conditions':terms_and_conditions,
    }
    return render(request, 'general/index.html', context)

def UpdateCityView(request):
    CityFormset = modelformset_factory(coremodels.city, extra=2, fields = '__all__')
    if request.method == 'POST':
        formset = CityFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        return redirect('customadmin:general')
    else:
        formset = CityFormset()
        context = {
            'formset':formset,
        }
        return render(request, 'general/city_formset.html', context)

def AddTestimonialView(request):
    if request.method == 'POST':
        form = forms.TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect( 'customadmin:general')
    else:
        form = forms.TestimonialForm()
        context = {
            'form':form,
        }
        return render(request, 'general/testimonial_form.html', context)

def EditTestimonialView(request, id):
    testimonial = get_object_or_404(coremodels.testimonials, id=id)
    if request.method == 'POST':
        form = forms.TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
        return redirect('customadmin:general')
    else:
        form = forms.TestimonialForm(instance=testimonial)
        context = {
            'form': form,
        }
        return render(request, 'general/testimonial_form.html', context)

def DeleteTestimonialView(request, id):
    testimonial = get_object_or_404(coremodels.testimonials, id=id)
    testimonial.delete()
    return redirect( 'customadmin:general')

def AddMainPageBannersView(request):
    if request.method == 'POST':
        form = forms.BannersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect( 'customadmin:general')
    else:
        form = forms.BannersForm()
        context = {
            'form':form,
        }
        return render(request, 'general/banners_form.html', context)

def EditMainPageBannersView(request, id):
    banner = get_object_or_404(coremodels.banner, id=id)
    if request.method == 'POST':
        form = forms.BannersForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
        return redirect( 'customadmin:general')
    else:
        form = forms.BannersForm(instance=banner)
        context = {
            'form':form,
        }
        return render(request, 'general/banners_form.html', context)

def DeleteMainPageBannersView(request, id):
    banner = get_object_or_404(coremodels.banner, id=id)
    banner.delete()
    return redirect( 'customadmin:general')

def UpdateFAQsView(request):
    FAQFormset = modelformset_factory(coremodels.faq, fields = '__all__')
    if request.method == 'POST':
        formset = FAQFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        redirect( 'customadmin:general')
    else:
        formset = FAQFormset(request.POST, request.FILES)
        context = {
            'formset':formset,
        }
        return render(request, 'general/faqs_formset.html', context)

def UpdateTermsAndConditionsView(request):
    TermsAndConditionsFormset = modelformset_factory(coremodels.TermsAndConditions, fields = '__all__')
    if request.method == 'POST':
        formset = TermsAndConditionsFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        redirect( 'customadmin:general')
    else:
        formset = TermsAndConditionsFormset(request.POST, request.FILES)
        context = {
            'formset':formset,
        }
        return render(request, 'general/terms&conditions_formset.html', context)

def ContactUsView(request):
    contact_us = coremodels.contact.objects.all()
    context = {
        'contact_us':contact_us,
    }
    return render(request, 'general/contact_us.html', context)

def PaymentsView(request):
    payments = coremodels.payment.objects.all()
    context = {
        'payments':payments,
    }
    return render(request, 'general/payments.html', context)


# CAR SELECTION PAGE VIEWS
def CarTypePageViews(request):
    context = {}
    return render(request, 'car_type/index.html', context)

def UpdateCarAttributes(request):
    CarAtrributeFormset = modelformset_factory(coremodels.car_attr, fields = '__all__')
    if request.method == 'POST':
        formset = CarAtrributeFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:car_type')
    else:
        formset = CarAtrributeFormset()
        context = {
            'formset':formset,
        }
        return render(request, 'car_type/car_attribute_formset.html', context)

def UpdateCarAttributeValueView(request, id):
    CarAtrributeValueFormset = modelformset_factory(coremodels.car_attr_comparison, fields = '__all__')
    if request.method == 'POST':
        formset = CarAtrributeValueFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:car_type')
    else:
        formset = CarAtrributeValueFormset()
        context = {
            'formset':formset,
        }
        return render(request, 'car_type/car_attribute_value_formset.html', context)

def UpdateRideAdditionalChoices(request):
    RideAdditionalChoicesFormset = modelformset_factory(coremodels.ride_choices, fields='__all__')
    if request.method == 'POST':
        formset = RideAdditionalChoicesFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:car_type')
    else:
        formset = RideAdditionalChoicesFormset()
        context = {
            'formset':formset,
        }
    return render(request, 'car_type/additional_choices_formset.html', context)

def UpdateCityRideAttributeValues(request):
    RideAdditionalChoicesFormset = modelformset_factory(coremodels.ride_choices, fields= '__all__')
    if request.method == 'POST':
        formset = RideAdditionalChoicesFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:car_type')
    else:
        formset = RideAdditionalChoicesFormset()
        context = {
            'formset':formset,
        }
    return render(request, 'car_type/city_ride_attributes_formset.html', context)


# Popular Destinations View
def PopularDestinationsView(request):
    popular_destinations = coremodels.popular_destinations.objects.all()
    context = {
        'popular_destinations':popular_destinations,
    }
    return render(request, 'popular_destinations/index.html', context)

def AddPopularDestinationView(request):
    if request.method == 'POST':
        form = forms.PopularDestinationsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect( 'customadmin:popular_destinations')
    else:
        form = forms.PopularDestinationsForm()
        context = {
            'form':form,
        }
        return render(request, 'popular_destinations/form.html', context)

def EditPopularDestinationView(request, id):
    popular_destination = get_object_or_404(coremodels.popular_destinations, id=id)
    if request.method == 'POST':
        form = forms.PopularDestinationsForm(request.POST, request.FILES, instance=popular_destination)
        if form.is_valid():
            form.save()
        return redirect( 'customadmin:popular_destinations')
    else:
        form = forms.PopularDestinationsForm(instance=popular_destination)
        context = {
            'form':form,
        }
        return render(request, 'popular_destinations/form.html', context)

def DeletePopularDestinationView(request):
    popular_destination = get_object_or_404(coremodels.popular_destinations, id=id)
    popular_destination.delete()
    return redirect( 'customadmin:popular_destinations')


# BLOG VIEWS
def BlogsView(request):
    categories = blogmodels.categories.objects.all()
    context = {
        'categories':categories,
    }
    return render(request, 'blogs/index.html', context)

def UpdateBlogCategoriesView(request):
    CategoriesFormset = modelformset_factory(blogmodels.categories, fields='__all__', extra=2)
    if request.method == 'POST':
        formset = CategoriesFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect( 'customadmin:blogs')
    else:
        formset = CategoriesFormset()
        context = {
            'formset':formset,
        }
        return render(request, 'blogs/categories_formset.html', context)

def AddBlogPostView(request):
    if request.method == 'POST':
        form = forms.BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request, 'Blog Post added successfully')
            return redirect( 'customadmin:blogs')
        else:
            messages.error(request, 'Blog Post not added successfully')
            return redirect( 'customadmin:blogs')
    else:
        form = forms.BlogPostForm()
        context = {
            'form':form,
        }
        return render(request, 'blogs/blog_form.html', context)

def EditBlogPostView(request, id):
    post = get_object_or_404(blogmodels.post, id = id)
    if request.method == 'POST':
        form = forms.BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog Post added successfully')
            return redirect( 'customadmin:blogs')
        else:
            messages.error(request, 'Blog Post not added successfully')
            return redirect( 'customadmin:blogs')
    else:
        form = forms.BlogPostForm(instance=post)
        context = {
            'form':form,
        }
        return render(request, 'blogs/blog_form.html', context)

def DeleteBlogPostView(request, id):
    post = get_object_or_404(blogmodels.post, id=id)
    post.delete()
    messages.success(request, 'Blog Post Deleted successfully')
    return redirect( 'customadmin:blogs')

def DeleteBlogPostCommentView(request, id):
    comment = get_object_or_404(blogmodels.comment, id=id)
    comment.delete()
    messages.success(request, 'Blog Post Comment Deleted successfully')
    return redirect( 'customadmin:blogs')


# CUSTOMER VIEWS
def CustomersView(request):
    customers = customermodels.customerprofile.objects.all()
    context = {
        'customers':customers,
    }
    return render(request, 'customers/index.html', context)

def AddCustomerView(request):
    if request.method == 'POST':
        userform = forms.UserForm(request.POST, request.FILES)
        profileform = forms.CustomerForm(request.POST, request.FILES)
        if userform.is_valid():
            new_form = userform.save(commit=False)
            new_form.username = str(userform.cleaned_data['mobile'])
            new_form.set_password(str(userform.cleaned_data['mobile']))
            new_form.save()
            if profileform.is_valid():
                new_form = profileform.save(commit=False)
                new_form.user = new_form
                profileform.save()
        return redirect(request, 'customadmin:customers')
    else:
        userform = forms.UserForm()
        profileform = forms.CustomerForm()
        context = {
            'profileform':profileform,
            'userform':userform,
        }
        return render(request, 'customers/customer_form.html', context)

def EditCustomerView(request, id):
    profile = get_object_or_404(customermodels.customerprofile, id=id)
    user = profile.user
    if request.method == 'POST':
        userform = forms.UserForm(request.POST, request.FILES, instance=user)
        profileform = forms.CustomerForm(request.POST, request.FILES, instance=profile)
        if userform.is_valid():
            userform.save()
        if profileform.is_valid():
            profileform.save()
        return redirect( 'customadmin:customers')
    else:
        userform = forms.UserForm(instance=user)
        profileform = forms.CustomerForm(instance=profile)
        context = {
            'profileform':profileform,
            'userform':userform,
        }
        return render(request, 'customers/customer_form.html', context)

def DeleteCustomerView(request, id):
    profile = get_object_or_404(customermodels.customerprofile, id=id)
    user = profile.user
    profile.delete()
    user.delete()
    return redirect( 'customadmin:customers')

def UpdateCustomerPromotionalView(request, id):
    profile = get_object_or_404(customermodels.customerprofile, id=id)
    CustomerPromotionalFormset = inlineformset_factory(customermodels.customerprofile, customermodels.customer_promotional, exclude=['customer'], extra=1)
    if request.method == 'POST':
        formset = CustomerPromotionalFormset(request.POST, request.FILES, instance = profile)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Saved Successfully')
        return redirect( 'customadmin:customers')
    else:
        formset = CustomerPromotionalFormset(instance = profile)
        context = {
            'formset':formset,
        }
        return render(request, 'customers/promotionals_formset.html', context)


# Vendor Views
def VendorsView(request):
    vendors = vendormodels.vendorprofile.objects.all()
    context = {
        'vendors':vendors
    }
    return render(request, 'vendors/index.html', context)

def VendorView(request, id):
    vendor = get_object_or_404(vendormodels.vendorprofile, id=id)
    context = {
        'vendor':vendor,
    }
    return render(request, 'vendors/vendor.html', context)

def AddVendorView(request):
    if request.method == 'POST':
        userform = forms.UserForm(request.POST, request.FILES)
        profileform = forms.VendorForm(request.POST, request.FILES)
        if userform.is_valid():
            new_form = userform.save(commit=False)
            new_form.username = str(userform.cleaned_data['mobile'])
            new_form.set_password(str(userform.cleaned_data['mobile']))
            new_form.save()
            if profileform.is_valid():
                new_form = profileform.save(commit=False)
                new_form.user = new_form
                profileform.save()
        return redirect( 'customadmin:customers')
    else:
        userform = forms.UserForm()
        profileform = forms.VendorForm()
        context = {
            'userform':userform,
            'profileform':profileform,
        }
        return render(request, 'vendors/vendor_form.html', context)

def EditVendorView(request, id):
    profile = get_object_or_404(vendormodels.vendorprofile, id=id)
    user = profile.user
    if request.method == 'POST':
        userform = forms.UserForm(request.POST, request.FILES, instance=user)
        profileform = forms.VendorForm(request.POST, request.FILES, instance=profile)
        if userform.is_valid():
            userform.save()
        if profileform.is_valid():
            profileform.save()
        return redirect( 'customadmin:customers')
    else:
        userform = forms.UserForm(instance=user)
        profileform = forms.VendorForm(instance=profile)
        context = {
            'profileform':profileform,
            'userform':userform,
        }
        return render(request, 'vendors/vendor_form.html', context)

def DeleteVendorView(request):
    vendor = get_object_or_404(vendormodels.vendorprofile, id=id)
    vendor.delete()
    return redirect( 'customadmin:vendors')

def UpdateVendorCarsView(request, id):
    vendor = get_object_or_404(vendormodels.vendorprofile, id=id)
    CarsFormset = inlineformset_factory(vendormodels.vendorprofile, vendormodels.vendor_cars, exclude=['vendor'], extra=2)

    if request.method == 'POST':
        formset = CarsFormset(request.POST, request.FILES, instance = vendor)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:vendors')
    else:
        formset = CarsFormset(instance = vendor)
        context = {
            'formset':formset,
        }
        return render(request, 'vendors/vendor_car_formset.html', context)

def UpdateVendorDriversView(request, id):
    vendor = get_object_or_404(vendormodels.vendorprofile, id=id)
    DriversFormset = inlineformset_factory(vendormodels.vendorprofile, vendormodels.vendor_cars, exclude=['vendor'],
                                        extra=2)

    if request.method == 'POST':
        formset = DriversFormset(request.POST, request.FILES, instance=vendor)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:vendors')
    else:
        formset = DriversFormset(instance=vendor)
        context = {
            'formset': formset,
        }
        return render(request, 'vendors/vendor_driver_formset.html', context)

# def AddVendorCarView(request, id):
#     form = forms.VendorCarForm()
#     context = {
#         'form':form,
#     }
#     return render(request, 'vendors/vendor_car_formset.html', context)
#
# def EditVendorCarView(request, id):
#     context = {}
#     return render(request, 'vendors/vendor_car_formset.html', context)
#
# def DeleteVendorCarView(request, id):
#     context = {}
#     return render(request, '', context)
#
# def AddVendorDriver(request):
#     form = forms.VendorDriverForm()
#     context = {
#         'form':form,
#     }
#     return render(request, 'vendors/vendor_driver_formset.html', context)
#
# def EditVendorDriver(request, id):
#     context = {}
#     return render(request, 'vendors/vendor_driver_formset.html', context)
#
# def DeleteVendorDriver(request, id):
#     context = {}
#     return render(request, '', context)






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

