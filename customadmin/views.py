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
from django.db.models import Count


from . import models, forms
from core import models as coremodels
from blog import models as blogmodels
from customer import models as customermodels
from vendor import models as vendormodels


def HomeView(request):

    late_running_rides = coremodels.ride_booking.objects.filter(ride_status__in = ['Assigned Car/Driver'], pickup_datetime__lt =datetime.datetime.today())
    last_minute_rides = coremodels.ride_booking.objects.filter(ride_status__in = ['Assigned Car/Driver'], pickup_datetime__lt =(datetime.datetime.today()+datetime.timedelta(hours = 4)))
    upcoming_rides = coremodels.ride_booking.objects.filter(ride_status__in = ['Booked', 'Selected Vendors', 'Assigned Vendor'], pickup_datetime__lt =datetime.datetime.today())
    top_pickup_cities = coremodels.ride_booking.objects.values('pickup_city__name').order_by("-pickup_city__count").annotate(Count('pickup_city'))[:5]
    top_drop_cities = coremodels.ride_booking.objects.values('drop_city__name').order_by("-drop_city__count").annotate(Count('drop_city'))[:5]

    context = {
        'late_running_rides':late_running_rides,
        'last_minute_rides':last_minute_rides,
        'upcoming_rides':upcoming_rides,
        'top_drop_cities':top_drop_cities,
        'top_pickup_cities':top_pickup_cities,
    }
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
def RideBookingView(request, id):
    booking = get_object_or_404(coremodels.ride_booking, id=id)
    context = {
        'booking':booking,
    }
    return render(request, 'ride_bookings/ride_booking.html', context)

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
    return render(request, 'ride_bookings/booked_rides.html', context)

def AssignVendorRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(ride_status = 'Selected Vendors')
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/assign_vendor_rides.html', context)

def UpdateVendorBidsView(request, id):
    booking = get_object_or_404(coremodels.ride_booking, id = id)
    BidsFormset = inlineformset_factory(coremodels.ride_booking, coremodels.vendorbids, extra=0, can_delete=False, exclude=['booking', 'datetime'])
    if request.method == 'POST':
        formset = BidsFormset(request.POST, instance = booking)
        if formset.is_valid():
            formset.save()
        return redirect('customadmin:assign_vendor_rides')
    else:
        formset = BidsFormset(instance = booking)
        context = {
            'formset':formset,
        }
        return render(request, 'ride_bookings/vendor_bids_formset.html', context)

def UpcomingRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(ride_status__in = ['Assigned Vendor', 'Assigned Car/Driver'])
    late_bookings = coremodels.ride_booking.objects.filter(ride_status__in = ['Assigned Vendor', 'Assigned Car/Driver'], pickup_datetime__lt =datetime.datetime.today())
    context = {
        'bookings':bookings,
        'late_bookings':late_bookings,
    }
    return render(request, 'ride_bookings/upcoming_rides.html', context)

def OngoingRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(ride_status__in = ['Ongoing', 'Completed'])
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/ongoing_rides.html', context)

def CompletedRidesView(request):
    bookings = coremodels.ride_booking.objects.filter(ride_status = 'Verified')
    context = {
        'bookings':bookings,
    }
    return render(request, 'ride_bookings/completed_rides.html', context)

def AssignVendorsView(request, id):
    booking = coremodels.ride_booking.objects.get(id=id)
    if request.method == 'POST':
        form = forms.AssignVendors(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.booking = booking
            booking.ride_status = 'Selected Vendors'
            new_form.datetime = datetime.datetime.now()
            new_form.save()
            booking.save()
            form.save_m2m()
            # for vendor in new_form.vendors.all:
            #     vendorbid = coremodels.vendorbids.objects.create(booking=booking, vendor = vendor)
            #     vendorbid.max_bid = booking.ride_fare*(1-(new_form.commission/100))
            #     vendorbid.save()
        return redirect('customadmin:booked_rides')
    else:
        form = forms.AssignVendors()
        context = {
            'form':form,
        }
        return render(request, 'ride_bookings/assign_vendors_form.html', context)


def AssignFinalVendorView(request, id):
    bid = get_object_or_404(coremodels.vendorbids, id=id)
    booking = bid.booking
    try:
        final_ride = coremodels.final_ride_detail.objects.get(booking = booking)
    except:
        final_ride = coremodels.final_ride_detail.objects.create(booking=booking, bid = bid)
    final_ride.save()
    booking.ride_status = "Assigned Vendor"
    booking.save()
    return redirect('customadmin:assign_vendor_rides')

def AssignDriverCarView(request, id):
    final_ride = get_object_or_404(coremodels.final_ride_detail, id= id)
    vendor = final_ride.bid.vendor
    cars = vendormodels.vendor_cars.objects.filter(vendor = vendor)
    drivers = vendormodels.driver.objects.filter(vendor = vendor)
    if request.method == 'POST':
        form = forms.AssignDriverCar(request.POST, request.FILES, instance = final_ride)
        if form.is_valid():
            form.save()
            final_ride.booking.ride_status = "Assigned Car/Driver"
            final_ride.booking.save()

            customer_message = "We have assigned Driver Name: " + str(final_ride.driver.full_name) + " (" + str(
                final_ride.driver.contact1) + ") " + "and Car Number: " + str(final_ride.car.registration_no)
            SMS(str(booking.phone_no), customer_message)

            driver_message = "You have been assigned to " + str(booking.name) + " (" + str(
                booking.phone_no) + " ) for " + str(booking.ride_type) + " ride, on dated " + str(
                booking.pickup_datetime) + " from " + str(booking.pickup_city) + " to " + str(booking.drop_city)
            SMS(str(final_ride.driver.contact1), driver_message)

        return redirect('customadmin:upcoming_rides')
    else:
        form = forms.AssignDriverCar(instance = final_ride)
        form.fields['car'].queryset = cars
        form.fields['driver'].queryset = drivers
        context = {
            'form':form,
        }
        return render(request, 'ride_bookings/assign_driver_car_form.html', context=context)

def StartRideView(request, id):
    final_ride = get_object_or_404(coremodels.final_ride_detail, id=id)
    vendor = final_ride.bid.vendor
    cars = vendormodels.vendor_cars.objects.filter(vendor=vendor)
    drivers = vendormodels.driver.objects.filter(vendor=vendor)
    if request.method == 'POST':
        form = forms.FinalRideForm(request.POST, request.FILES, instance=final_ride)
        if form.is_valid():
            form.save()
            final_ride.start_datetime = timezone.now()
            final_ride.booking.ride_status = "Ongoing"
            final_ride.booking.save()
            final_ride.save()
        return redirect('customadmin:upcoming_rides')
    else:
        form = forms.FinalRideForm(instance=final_ride)
        form.fields['car'].queryset = cars
        form.fields['driver'].queryset = drivers
        context = {
            'form': form,
        }
        return render(request, 'ride_bookings/start_ride_form.html', context=context)


def EndRideView(request, id):
    final_ride = get_object_or_404(coremodels.final_ride_detail, id=id)
    vendor = final_ride.bid.vendor
    cars = vendormodels.vendor_cars.objects.filter(vendor=vendor)
    drivers = vendormodels.driver.objects.filter(vendor=vendor)

    if request.method == 'POST':
        form = forms.FinalRideForm(request.POST, request.FILES, instance=final_ride)
        if form.is_valid():
            form.save()
            final_ride.end_datetime = timezone.now()
            final_ride.booking.ride_status = "Completed"
            final_ride.booking.save()
            final_ride.save()
        return redirect('customadmin:ongoing_rides')
    else:
        form = forms.FinalRideForm(instance=final_ride)
        form.fields['car'].queryset = cars
        form.fields['driver'].queryset = drivers
        context = {
            'form': form,
            'final_ride':final_ride,
        }
        return render(request, 'ride_bookings/end_ride_form.html', context=context)

def VerifyRideView(request, id):
    final_ride = get_object_or_404(coremodels.final_ride_detail, id=id)
    booking = final_ride.booking
    booking.ride_status = "Verified"
    booking.save()
    return redirect('customadmin:ongoing_rides')

def FinalRideDetailsView(request, id):
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
    CityFormset = modelformset_factory(coremodels.city, extra=2, fields = '__all__', can_delete=True)
    if request.method == 'POST':
        formset = CityFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

            cities = coremodels.city.objects.all()
            car_types = coremodels.car_types.objects.all()
            cal_attr = coremodels.calc_attr.objects.all()

            for pickup_cities in cities:
                if pickup_cities.pickup:
                    for dropcities in cities:
                        if dropcities.drop:
                            for type in car_types:
                                for attr in cal_attr:
                                    if attr.active:
                                        try:
                                            new = coremodels.calc_city_attr_value.objects.get(city1=pickup_cities,
                                                                                          city2=dropcities,
                                                                                          car_type=type,
                                                                                          attr=attr)
                                        except:
                                            new = coremodels.calc_city_attr_value.objects.create(city1=pickup_cities,
                                                                                             city2=dropcities,
                                                                                             car_type=type,
                                                                                             attr=attr,
                                                                                             value=attr.value)
                                            new.save()
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
    FAQFormset = modelformset_factory(coremodels.faq, fields = '__all__', can_delete=True, extra=1)
    if request.method == 'POST':
        formset = FAQFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:general')
    else:
        formset = FAQFormset()
        context = {
            'formset':formset,
        }
        return render(request, 'general/faqs_formset.html', context)

def UpdateTermsAndConditionsView(request):
    TermsAndConditionsFormset = modelformset_factory(coremodels.TermsAndConditions, fields = '__all__', can_delete=True)
    if request.method == 'POST':
        formset = TermsAndConditionsFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:general')
    else:
        formset = TermsAndConditionsFormset()
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
    bookings = coremodels.ride_booking.objects.filter(ride_status='Verified')
    context = {
        'bookings': bookings,
    }
    return render(request, 'general/payments.html', context)


# CAR SELECTION PAGE VIEWS
def CarTypePageViews(request):
    car_attrs = coremodels.car_attr.objects.all()
    car_types = coremodels.car_types.objects.all()
    ride_additional_choices = coremodels.ride_choices.objects.all()
    city_ride_attribute_values = coremodels.calc_city_attr_value.objects.all()
    pickup_cities = coremodels.city.objects.all()
    drop_cities = coremodels.city.objects.all()
    context = {
        'car_attrs':car_attrs,
        'car_types':car_types,
        'ride_additional_choices':ride_additional_choices,
        'city_ride_attribute_values':city_ride_attribute_values,
        'pickup_cities':pickup_cities,
        'drop_cities':drop_cities,
    }
    return render(request, 'car_type/index.html', context)

def UpdateCarAttributes(request):
    CarAtrributeFormset = modelformset_factory(coremodels.car_attr, fields = '__all__')
    if request.method == 'POST':
        formset = CarAtrributeFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

            car_types = coremodels.car_types.objects.all()
            car_attributes = coremodels.car_attr.objects.all()
            for car_type in car_types:
                for car_attribute in car_attributes:
                    try:
                        value = coremodels.car_attr_comparison.objects.get(car_type=car_type,
                                                                              attr_name=car_attribute)
                    except:
                        value = coremodels.car_attr_comparison.objects.create(car_type=car_type, attr_name = car_attribute, value='-')

        return redirect( 'customadmin:car_type')
    else:
        formset = CarAtrributeFormset()
        context = {
            'formset':formset,
        }
        return render(request, 'car_type/car_attribute_formset.html', context)

def UpdateCarAttributeValueView(request):
    CarAtrributeValueFormset = modelformset_factory(coremodels.car_attr_comparison, fields = '__all__', can_delete=False, extra=0)


    if request.method == 'POST':
        formset = CarAtrributeValueFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect( 'customadmin:car_type')
        else:
            return redirect('customadmin:update_car_attribute_values')
    else:
        formset = CarAtrributeValueFormset()
        qs = coremodels.car_attr_comparison.objects.all()

        selected_car_types = []
        selected_attributes = []

        if 'car_types' in request.GET:
            selected_car_types = list(request.GET.getlist('car_types'))
            qs = qs.filter(car_type_id__in = selected_car_types)

        if 'attributes' in request.GET:
            selected_attributes = list(request.GET.getlist('attributes'))
            qs = qs.filter(attr_name_id__in = selected_attributes)

        print(selected_car_types)
        print(selected_attributes)
        car_types = coremodels.car_types.objects.all()
        attributes = coremodels.car_attr.objects.all()
        formset.queryset = qs
        context = {
            'formset':formset,
            'car_types':car_types,
            'attributes':attributes,
            'selected_car_types':selected_car_types,
            'selected_attributes':selected_attributes,
        }
        return render(request, 'car_type/car_attribute_value_formset.html', context)

def UpdateRideAdditionalChoices(request):
    RideAdditionalChoicesFormset = modelformset_factory(coremodels.ride_choices, fields='__all__', can_delete=True)
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
    CityRideAttributesFormset = modelformset_factory(coremodels.calc_city_attr_value, fields= '__all__', extra=0, can_delete=False)
    if request.method == 'POST':
        formset = CityRideAttributesFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        return redirect( 'customadmin:car_type')
    else:
        formset = CityRideAttributesFormset()
        qs = coremodels.calc_city_attr_value.objects.all()

        selected_pickup_cities = []
        selected_drop_cities = []
        selected_car_types = []
        selected_attributes = []

        if 'pickup_cities' in request.GET:
            selected_pickup_cities = list(request.GET.getlist('pickup_cities'))
            qs = qs.filter(city1_id__in = selected_pickup_cities)

        if 'drop_cities' in request.GET:
            selected_drop_cities = list(request.GET.getlist('drop_cities'))
            qs = qs.filter(city2_id__in=selected_drop_cities)

        if 'car_types' in request.GET:
            selected_car_types = list(request.GET.getlist('car_types'))
            qs = qs.filter(car_type_id__in=selected_car_types)

        if 'attributes' in request.GET:
            selected_attributes = list(request.GET.getlist('attributes'))
            qs = qs.filter(attr_id__in=selected_attributes)

        formset.queryset = qs
        pickup_cities = coremodels.city.objects.filter(pickup = True)
        drop_cities = coremodels.city.objects.filter(pickup = True)
        car_types = coremodels.car_types.objects.all()
        attributes = coremodels.calc_attr.objects.all()
        context = {
            'formset':formset,
            'pickup_cities':pickup_cities,
            'drop_cities':drop_cities,
            'car_types':car_types,
            'attributes':attributes,
            'selected_pickup_cities':selected_pickup_cities,
            'selected_drop_cities':selected_drop_cities,
            'selected_car_types':selected_car_types,
            'selected_attributes':selected_attributes,
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
    CategoriesFormset = modelformset_factory(blogmodels.categories, fields='__all__', extra=2, can_delete=True)
    if request.method == 'POST':
        formset = CategoriesFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect( 'customadmin:blogs')
        else:
            print(formset.errors)
            print(formset.non_form_errors())
            return redirect('customadmin:blogs')
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
    profile = get_object_or_404(coremodels.User, id=id)
    CustomerPromotionalFormset = inlineformset_factory(coremodels.User, coremodels.user_referral, exclude=['customer'], extra=1, can_delete=True)
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
        return redirect('customadmin:vendors')
    else:
        userform = forms.UserForm()
        profileform = forms.VendorForm()
        context = {
            'userform':userform,
            'profileform':profileform,
        }
        return render(request, 'vendors/vendor_form.html', context)

def UpdateVendorStatusView(request, id):
    profile = get_object_or_404(vendormodels.vendorprofile, id=id)
    user = profile.user
    if request.method == 'POST':
        userform = forms.UserForm(request.POST, request.FILES, instance=user)
        form = forms.VendorForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('customadmin:vendors')
    else:
        userform = forms.UserForm(instance=user)
        form = forms.VendorForm(instance=profile)
        context = {
            'form':form,
            'userform':userform,
        }
        return render(request, 'vendors/vendor_status_form.html', context)

def EditVendorView(request, id):
    profile = get_object_or_404(vendormodels.vendorprofile, id=id)
    user = profile.user
    if request.method == 'POST':
        userform = forms.UserForm(request.POST, request.FILES, instance=user)
        profileform = forms.VendorForm(request.POST, request.FILES, instance=profile)
        if profileform.is_valid():
            profileform.save()
        return redirect('customadmin:vendor', id)
    else:
        userform = forms.UserForm(instance=user)
        form = forms.VendorForm(instance=profile)
        context = {
            'form':form,
            'userform':userform,
        }
        return render(request, 'vendors/vendor_form.html', context)

def DeleteVendorView(request):
    vendor = get_object_or_404(vendormodels.vendorprofile, id=id)
    vendor.delete()
    return redirect('customadmin:vendors')

def AddVendorCarView(request, id):
    vendor = get_object_or_404(vendormodels.vendorprofile, id=id)
    if request.method == 'POST':
        form = forms.VendorCarForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.vendor = vendor
            new_form.save()
        return redirect('customadmin:vendor', vendor.id)
    else:
        form = forms.VendorCarForm()
        context = {
            'form':form,
        }
        return render(request, 'vendors/car_form.html', context)

def EditVendorCarView(request, id):
    car = get_object_or_404(vendormodels.vendor_cars, id=id)
    if request.method == 'POST':
        form = forms.VendorCarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
        return redirect('customadmin:vendor', car.vendor.id)
    else:
        form = forms.VendorCarForm(instance=car)
        context = {
            'form':form,
        }
        return render(request, 'vendors/car_form.html', context)

def DeleteVendorCarView(request, id):
    car = get_object_or_404(vendormodels.vendor_cars, id = id)
    vendor = car.vendor
    car.delete()
    return redirect('customadmin:vendor', vendor.id)

def AddVendorDriver(request):
    vendor = get_object_or_404(vendormodels.vendorprofile, id=id)
    if request.method == 'POST':
        form = forms.VendorDriverForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.vendor = vendor
            new_form.save()
        return redirect('customadmin:vendor', vendor.id)
    else:
        form = forms.VendorDriverForm()
        context = {
            'form':form,
        }
        return render(request, 'vendors/driver_form.html', context)

def EditVendorDriver(request, id):
    driver = get_object_or_404(vendormodels.driver, id=id)
    if request.method == 'POST':
        form = forms.VendorDriverForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Details updated successfully')
            return redirect('customadmin:vendor', driver.vendor.id)
        else:
            messages.error(request, 'Please check the details.')

    form = forms.VendorDriverForm(instance=driver)
    context = {
        'form':form,
    }
    return render(request, 'vendors/driver_form.html', context)

def DeleteVendorDriver(request, id):
    driver = get_object_or_404(vendormodels.driver, id=id)
    vendor = driver.vendor
    driver.delete()
    return redirect('customadmin:vendor', vendor.id)

def UpdateVendorBankDetailsView(request, id):
    vendor = get_object_or_404(vendormodels.vendorprofile, id=id)
    BankDetailsFormset = inlineformset_factory(vendormodels.vendorprofile, vendormodels.bank_detail, exclude=['vendor'],
                                        extra=2)

    if request.method == 'POST':
        formset = BankDetailsFormset(request.POST, request.FILES, instance=vendor)
        if formset.is_valid():
            formset.save()
        return redirect('customadmin:vendor', vendor.id)
    else:
        formset = BankDetailsFormset(instance=vendor)
        context = {
            'formset': formset,
        }
        return render(request, 'vendors/vendor_bank_formset.html', context)









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

