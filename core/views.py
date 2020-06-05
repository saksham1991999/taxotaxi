from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, render_to_response
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils import timezone
from django.template import Context, Template,RequestContext
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()
from customer import models as customermodels
from .oneway_calc import oneway_calculator
from .airport_calc import airport_calculator
import datetime, hashlib, random, requests
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from core.payu import PAYU
payu = PAYU()
import dateutil.parser
MERCHANT_KEY = 'QxL9PGUue%ZdByvX'

# def distanceapi(placeid1, placeid2):
#     placeid1 = 'ChIJiR6elYwXDTkRuTEotblJ6VE'
#     placeid2 = 'ChIJ46KtIxkbDTkR_tKtGAWTaRE'
#
#     api_key = 'AIzaSyAkvnTgO3zgaBKBSGNLKi7H5YPSOFYfrmU'
#
#     url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
#
#     r = requests.get(url + 'origins=place_id:' + placeid1 + '&destinations=place_id:' + placeid2 + '&type='
#                      '&units=metric' +'&key=' + api_key)
#
#     x = r.json()
#     y = x['rows']
#     print(x)
#     print(y)
#
#     api_key = 'AIzaSyAkvnTgO3zgaBKBSGNLKi7H5YPSOFYfrmU'
#
#     url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
#
#     r = requests.get(url + 'origins=place_id:' + placeid1 + '&destinations=place_id:' + placeid2 + '&type='
#                                                                                                    '&units=metric' + '&key=' + api_key)


def SSLView(request):
    return HttpResponse('7h6nnz946n5klbywjzw15lvhtnvbzf64')

def TestView(request):
    context = {}
    return render(request, 'test_template.html', context)

def SMS(mobile, message):
    mobile = '91' + str(mobile)
    message = str(message)
    url = 'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=fsdCr1FyckqYrndE63halg&senderid=SMSTST&channel=2&DCS=0&flashsms=0&number='+mobile+'&text='+message+'&route=1'
    print(url)
    r = requests.post(url = url)
    x = r.text
    print(x)

def distance_time(pickup, drop):
    api_key = 'AIzaSyAkvnTgO3zgaBKBSGNLKi7H5YPSOFYfrmU'
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    r = requests.get(url, params={
        'origins': pickup,
        'destinations': drop,
        'type=': '',
        'units': 'metric',
        'key': api_key,
    })
    #print(r)
    x = r.json()
    #print(x)
    rows = x['rows']
    elements = rows[0]['elements']
    distance = ((elements[0]['distance'])['value']) / 1000
    duration = ((elements[0]['duration'])['value']) / 60

    distance_text = ((elements[0]['distance'])['text'])
    duration_text = ((elements[0]['duration'])['text'])

    #print(distance)
    #print(duration)
    return distance, duration, distance_text, duration_text

def places():

    # api_key = 'AIzaSyAkvnTgO3zgaBKBSGNLKi7H5YPSOFYfrmU'
    api_key = 'AIzaSyCs6vwYNGR2f-CiKEvipu1UWOmkKy7Vdlk'

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    city = ' gurgaon'
    query = input('Search query: ')
    query += city
    print(query)
    r = requests.get(url + 'input=' + query + '&fields=formatted_address,name,place_id' + '&key=' + api_key)

    x = r.json()
    print(x)
    y = x['results']
    print(y)
    for i in range(len(y)):
        print(y[i]['name'])
        print(y[i]['formatted_address'])
        print(y[i]['place_id'])




def ComingSoonView(request):
    context = {}
    return render(request, 'coming_soon.html', context)

def HomeView(request):
    if request.method == 'POST':
        if 'form_type' in request.POST:
            form_type = request.POST['form_type']
            if form_type == 'contact-us':
                contactform = forms.ContactForm(request.POST)

                if contactform.is_valid():
                    contactform.save()
                    name = 'Guest'
                    if request.user.is_authenticated:
                        name = request.user.first_name
                    messages.success(
                        request,
                        'Dear ' + str(name) + ', Thank you for contacting TaxoTaxi, we will get back to you soon.',
                        extra_tags='alert alert-success alert-dismissible'
                    )
                return redirect('core:home')
        else:
            ride_type = request.POST['type']
            request.session['ride_type'] = ride_type

            # DateTime
            pickup_datetime = request.POST['pickup_datetime']
            pickup_date, pickup_time = pickup_datetime.split()
            d, m, y = pickup_date.split('-')

            hr, min = pickup_time.split(':')
            # if am_pm.upper() == 'PM' and hr != '12':
            #     hr = int(hr) + 12
            # if am_pm.upper() == 'AM' and hr == '12':
            #     hr = 0
            pickup_datetime = datetime.datetime(year=int(y), month=int(m), day=int(d), hour=int(hr), minute=int(min),
                                                second=00,
                                                microsecond=00)

            if ride_type == 'One Way':
                pickup_city = request.POST['pickup_city']
                drop_city = request.POST['drop_city']
                pickup = request.POST['pickup']
                drop = request.POST['drop']
                pickup_city = models.city.objects.get(name=pickup_city)
                drop_city = models.city.objects.get(name=drop_city)

                distance, duration, distance_text, duration_text = distance_time(pickup, drop)

                # Calculator Called
                final_prices, price_km, drop_datetime, initial_charges, additional_charges, early_pickup_charges, late_drop_charges, night_charges, gst_charges = oneway_calculator(pickup_city, drop_city, distance, duration,
                                                                          pickup_datetime)

                # ride_type = 'One Way'
                # pickup_city = 'Gurgaon'
                # drop_city = 'Faridabad'
                # pickup = 'Sector 10A Gurgaon'
                # drop = 'BK Chowk Faridabad'
                # pickup_datetime = datetime.datetime.now().__str__()
                # drop_datetime = datetime.datetime.now().__str__()
                # duration = 1232
                # distance = 32
                # car_type = 'compact'
                # ride_checkboxes = ['1', '2']
                # ride_total = 234
                # distance_text = '32 Km'
                # duration_text = '1 Hour'
                # final_prices = [500, 700, 900]
                # price_km = [9,10,12]
                request.session['ride_type'] = ride_type
                request.session['pickup_city'] = pickup_city.name
                request.session['drop_city'] = drop_city.name
                request.session['pickup'] = pickup
                request.session['drop'] = drop
                request.session['pickup_datetime'] = pickup_datetime.__str__()
                request.session['drop_datetime'] = drop_datetime.__str__()
                request.session['duration'] = duration
                request.session['distance'] = distance
                request.session['distance_text'] = distance_text
                request.session['duration_text'] = duration_text

                request.session['final_prices_list'] = final_prices
                request.session['price_km_list'] = price_km
                request.session['initial_charges_list'] = initial_charges
                request.session['initial_charges_list'] = initial_charges
                request.session['additional_charges_list'] = additional_charges
                request.session['early_pickup_charges_list'] = early_pickup_charges
                request.session['late_drop_charges_list'] = late_drop_charges
                request.session['night_charges_list'] = night_charges
                request.session['gst_charges_list'] = gst_charges

            elif ride_type == 'Airport':
                pickup_city = request.POST['pickup_city']
                drop_city = request.POST['drop_city']
                pickup = request.POST['pickup']
                drop = request.POST['drop']
                pickup_city = models.city.objects.get(name=pickup_city)
                drop_city = models.city.objects.get(name=drop_city)

                distance, duration, distance_text, duration_text = distance_time(pickup, drop)

                final_prices, price_km, drop_datetime, initial_charges, additional_charges, early_pickup_charges, late_drop_charges, night_charges, gst_charges = airport_calculator(pickup_city, drop_city, distance, duration,
                                                                          pickup_datetime)
                request.session['ride_type'] = ride_type
                request.session['pickup_city'] = pickup_city.name
                request.session['drop_city'] = drop_city.name
                request.session['pickup'] = pickup
                request.session['drop'] = drop
                request.session['pickup_datetime'] = pickup_datetime.__str__()
                request.session['drop_datetime'] = drop_datetime.__str__()
                request.session['duration'] = duration
                request.session['distance'] = distance
                request.session['distance_text'] = distance_text
                request.session['duration_text'] = duration_text

                request.session['final_prices_list'] = final_prices
                request.session['price_km_list'] = price_km
                request.session['initial_charges_list'] = initial_charges
                request.session['initial_charges_list'] = initial_charges
                request.session['additional_charges_list'] = additional_charges
                request.session['early_pickup_charges_list'] = early_pickup_charges
                request.session['late_drop_charges_list'] = late_drop_charges
                request.session['night_charges_list'] = night_charges
                request.session['gst_charges_list'] = gst_charges

            return redirect('core:cars')

    else:
        testimonials = models.testimonials.objects.all()[:6]
        pickup_cities = models.city.objects.filter(pickup=True)
        drop_cities = models.city.objects.filter(drop=True)
        banners = models.banner.objects.all()
        contactform = forms.ContactForm()
        popular_destinations = models.popular_destinations.objects.all()
        context = {
            'testimonials':testimonials,
            'pickup_cities':pickup_cities,
            'drop_cities':drop_cities,
            'banners':banners,
            'popular_destinations':popular_destinations,

            'contactform':contactform,
        }
        return render(request, 'index.html', context)


def CarSpecificationsView(request):
    ride_type = request.session['ride_type']
    pickup_city = request.session['pickup_city']
    drop_city = request.session['drop_city']
    pickup = request.session['pickup']
    drop = request.session['drop']
    pickup_datetime = request.session['pickup_datetime']
    drop_datetime = request.session['drop_datetime']
    duration = request.session['duration']
    distance = request.session['distance']
    distance_text = request.session['distance_text']
    duration_text = request.session['duration_text']

    price_km = request.session['price_km_list']
    initial_charges = request.session['initial_charges_list']

    pickup_datetime = dateutil.parser.parse(pickup_datetime)
    drop_datetime = dateutil.parser.parse(drop_datetime)
    # pickup_datetime = datetime.datetime.fromisoformat(pickup_datetime)

    if request.method == 'POST':
        car_type = request.POST['car_type']
        car_type_id = models.car_types.objects.get(name=car_type).id

        ride_checkboxes = []
        final_prices = request.session['final_prices_list']
        ride_total = final_prices[car_type_id - 1]

        initial_charges = request.session['initial_charges_list'][car_type_id - 1]
        additional_charges = request.session['additional_charges_list'][car_type_id - 1]
        early_pickup_charges = request.session['early_pickup_charges_list'][car_type_id - 1]
        late_drop_charges = request.session['late_drop_charges_list'][car_type_id - 1]
        night_charges = request.session['night_charges_list'][car_type_id - 1]
        gst_charges = request.session['gst_charges_list'][car_type_id - 1]

        checkbox_charges = 0
        try:
            ride_checkboxes = request.POST.getlist('ride_checkboxes')
            print(ride_checkboxes, type(ride_checkboxes))
            for ride_checkbox in ride_checkboxes:
                checkbox_charge = int(models.ride_choices.objects.get(id=ride_checkbox).value)
                print(checkbox_charge)
                checkbox_charges += checkbox_charge
        except:
            pass
        print(ride_total, checkbox_charges)
        ride_total = ride_total + checkbox_charges

        car_type = models.car_types.objects.get(id=car_type_id).name

        request.session['car_type'] = car_type
        request.session['ride_checkboxes'] = ride_checkboxes
        request.session['checkbox_charges'] = checkbox_charges
        request.session['ride_total'] = ride_total

        request.session['final_prices'] = final_prices
        request.session['price_km'] = price_km
        request.session['initial_charges'] = initial_charges
        request.session['additional_charges'] = additional_charges
        request.session['early_pickup_charges'] = early_pickup_charges
        request.session['late_drop_charges'] = late_drop_charges
        request.session['night_charges'] = night_charges
        request.session['gst_charges'] = gst_charges

        return redirect('core:booking-login')
    else:
        ride_type_qs = models.ride_types.objects.get(name = ride_type)
        ride_checkboxes = models.ride_choices.objects.filter(ride_type__in=[ride_type_qs])
        car_attrs = models.car_attr.objects.all()
        car_types = models.car_types.objects.all()
        banners = models.banner.objects.all()

        context = {
            'ride_type': ride_type,
            'pickup_city': pickup_city,
            'drop_city': drop_city,
            'pickup': pickup,
            'drop': drop,
            'pickup_datetime': pickup_datetime,
            'drop_datetime': pickup_datetime,
            'duration': duration,
            'distance': distance,
            'distance_text': distance_text,
            'duration_text': duration_text,
            'ridecheckboxes': ride_checkboxes,
            'car_attrs': car_attrs,
            'car_types': car_types,

            'initial_charges': initial_charges,
            'city_price_km': price_km,
            'banners': banners,
        }
        return render(request, 'car_specifications.html', context)

def LoginView(request):
    logout(request)
    if request.method == 'POST':
        type = request.POST['type']
        mobile = request.POST['phone_num']
        password = request.POST['password']

        if type == 'login':
            try:
                user = authenticate(request, username=mobile, password=password)
                if user.mobile_verified:
                    login(request, user)
                    if user.is_vendor:
                        redirect('vendor:dashboard')
                    else:
                        return redirect('customer:dashboard')
                else:
                    otp = random.randint(1000, 9999)
                    request.session['mobile'] = mobile
                    request.session['password'] = password
                    request.session['otp'] = otp
                    text = 'T2T Hi ' + str(user.first_name) + ', Please use OTP ' + str(
                        otp) + ' to complete the registration process on taxotaxi.com'
                    SMS(mobile, text)
                    print('-----------------------OTP--------------------------')
                    print(otp)
                    return redirect('core:register_otp_verification')
            except:
                messages.error(request, 'Invalid Credentials', extra_tags = 'alert alert-warning alert-dismissible')
                return redirect('core:login')
        elif type == 'register':
            try:
                email = request.POST['email_id']
                full_name = request.POST['full_name']
                user = models.User.objects.create_user(username=mobile, email=email, password=password)
                lname = ''
                fname, lname = full_name.split()
                user.first_name = fname
                user.last_name = lname
                user.mobile = mobile
                user.save()

                otp = random.randint(1000, 9999)
                request.session['mobile'] = mobile
                request.session['password'] = password
                request.session['otp'] = otp
                text = 'T2T Hi ' + str(full_name) + ', Please use OTP ' + str(
                    otp) + ' to complete the registration process on taxotaxi.com'
                SMS(mobile, text)
                print('-----------------------OTP--------------------------')
                print(otp)

                customerprofile = customermodels.customerprofile.objects.create(user = user)
                referal_code = customermodels.customer_promotional.objects.create(customer = customerprofile, promotional_code=str(mobile), referralbenefit=50, customerbenefit=50, is_activated=True)


                return redirect('core:register_otp_verification')
            except:
                messages.error(request, 'Mobile Already Registered', extra_tags='alert alert-warning alert-dismissible')
        return redirect('core:login')
    else:
        context = {
        }
        return render(request, 'login.html', context)

def RegisterOTPVerification(request):
    if request.method == 'POST':
        input_otp = request.POST['otp']
        generated_otp = request.session['otp']
        if int(input_otp) == int(generated_otp):
            mobile = request.session['mobile']
            password = request.session['password']
            user = authenticate(username=mobile, password=password)
            login(request, user)
            user.mobile_verified = True
            user.save()
            return redirect('core:home')
        else:
            messages.error(request, "Inavlid OTP", extra_tags='alert alert-warning alert-dismissible')
            return redirect('core:register_otp_verification')
    else:
        mobile = request.session['mobile']
        context = {
            'mobile': mobile,
        }
        return render(request, 'register_otp.html', context)

def LogoutView(request):
    logout(request)
    return redirect('core:home')

@login_required(login_url='/login/')
def DashboardView(request):
    if request.user.is_vendor:
        return redirect('vendor:dashboard')
    else:
        return redirect('customer:dashboard')

def RegisterVendorAgentView(request):
    context = {}
    return render(request, 'Vendor/registration.html', context)

def ContactView(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            name = 'Guest'
            if request.user.is_authenticated:
                name = request.user.first_name
            messages.success(
                request,
                'Dear ' + str(name) + ', Thank you for contacting TaxoTaxi, we will get back to you soon.',
                extra_tags='alert alert-success alert-dismissible'
            )
        else:
            print(form.errors)
            print('form not valid')
        return redirect('core:contact')
    else:
        form = forms.ContactForm()
        context = {
            'contactform': form,
        }
        return render(request, 'contact.html', context)

def FAQView(request):
    faqs = models.faq.objects.all()
    context = {
        'questions':faqs,
    }
    return render(request, 'faq.html', context)

def TermsAndConditionsView(request):
    termsandconditions = models.TermsAndConditions.objects.all()
    context = {
        'termsandconditions':termsandconditions,
    }
    return render(request, 'terms&conditions.html' ,context)

def ForgotPasswordView(request):
    if request.method == 'POST':
        form = forms.ForgotPasswordForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            try:
                user = get_object_or_404(models.User, username=mobile)
            except:
                messages.error(request, 'This Mobile Number is not Registered with us.',  extra_tags='alert alert-error alert-dismissible' )
                # raise ValidationError(_("This Mobile Number is not Registered"))
                return redirect('core:forgot_password')
            otp = random.randint(1000, 9999)
            request.session['mobile'] = mobile
            request.session['otp'] = otp
            message = 'HI, ' + str(mobile) + '. Please use ' + str(otp) + " to complete your change password request. If you haven't requested, please ignore"
            SMS(str(mobile), message)
            return redirect('core:forgot_password_otp')
        else:
            raise ValidationError(_('Please Enter a Valid Phone Number'))
    else:
        form = forms.ForgotPasswordForm()
        context = {
            'form':form,
        }
        return render(request, 'Reset Password/forgot_password.html', context)

def ForgotPasswordOTPView(request):
    if request.method == 'POST':
        form = forms.ResetPasswordForm(request.POST)
        if form.is_valid():
            mobile = request.session['mobile']
            generated_otp = request.session['otp']
            otp_entered = form.cleaned_data['otp']
            new_password = form.cleaned_data['password1']
            if int(otp_entered) == int(generated_otp):
                user = get_object_or_404(models.User, username = mobile)
                user.set_password(new_password)
                user.save()
                user = authenticate(username=mobile, password=new_password)
                login(request, user)
                messages.success(request, 'Password Updated',  extra_tags='alert alert-success alert-dismissible')
                return redirect('core:home')
            else:
                messages.error(request, "Entered OTP is wrong !! Please enter correct OTP",  extra_tags='alert alert-error alert-dismissible')
                return redirect('core:forgot_password_otp')
                raise ValidationError(_("Entered OTP is wrong !! Please enter correct OTP"))
    else:
        form = forms.ResetPasswordForm()
        context = {
            'form':form,
        }
        return render(request, 'Reset Password/reset_password.html', context)

def CheckBoxesAdder(request):
    print('------------------------------ REQUEST -----------------------------------')
    print(request.POST)
    car_type = request.POST['car_type']
    car_type_id = models.car_types.objects.get(name=car_type).id

    ride_checkboxes = []
    final_prices = request.session['final_prices']
    ride_total = final_prices[car_type_id - 1]
    checkbox_charges = 0
    try:
        ride_checkboxes = request.POST.getlist('ride_checkboxes')
        print(ride_checkboxes, type(ride_checkboxes))
        for ride_checkbox in ride_checkboxes:
            checkbox_charge = int(models.ride_choices.objects.get(id=ride_checkbox).value)
            print(checkbox_charge)
            checkbox_charges += checkbox_charge
    except:
        pass
    print(ride_total, checkbox_charges)
    ride_total = ride_total + checkbox_charges

    car_type = models.car_types.objects.get(id=car_type_id).name
    request.session['car_type'] = car_type
    request.session['ride_total'] = ride_total
    request.session['ride_checkboxes'] = ride_checkboxes
    request.session['checkbox_charges'] = checkbox_charges
    return redirect('core:booking-login')

def CustomerLoginView(request):
    ride_type = request.session['ride_type']
    pickup_city = request.session['pickup_city']
    drop_city = request.session['drop_city']
    pickup = request.session['pickup']
    drop = request.session['drop']
    pickup_datetime = request.session['pickup_datetime']
    drop_datetime = request.session['drop_datetime']
    duration = request.session['duration']
    distance = request.session['distance']
    car_type = request.session['car_type']
    ride_checkboxes = request.session['ride_checkboxes']
    ride_total = request.session['ride_total']
    distance_text = request.session['distance_text']
    duration_text = request.session['duration_text']
    checkbox_charges = request.session['checkbox_charges']

    if request.user.is_authenticated:
        return redirect('core:checkout')
    else:
        pickup_datetime = dateutil.parser.parse(pickup_datetime)
        drop_datetime = dateutil.parser.parse(drop_datetime)
        context = {
            'ride_type': ride_type,
            'pickup_city': pickup_city,
            'drop_city': drop_city,
            'pickup': pickup,
            'drop': drop,
            'pickup_datetime': pickup_datetime,
            'drop_datetime': drop_datetime,
            'duration': duration,
            'distance': distance,
            'car_type': car_type,
            'ride_checkboxes': ride_checkboxes,
            'ride_total': ride_total,
            'distance_text': distance_text,
            'duration_text': duration_text,
            'checkbox_charges':checkbox_charges,
        }
        return render(request, 'customer_login_booking.html', context)

def CustomerAuthenticationView(request):
    if request.user.is_authenticated:
        return redirect('core:checkout')
    else:
        if request.method == 'POST':
            type = request.POST['type']
            mobile = request.POST['phone_num']
            password = request.POST['password']
            print(request.POST)
            if type == 'login':
                try:
                    user = authenticate(request, username=mobile, password=password)
                    if user.mobile_verified:
                        login(request, user)
                        return redirect('core:checkout')
                    else:
                        otp = random.randint(1000, 9999)
                        request.session['mobile'] = mobile
                        request.session['password'] = password
                        request.session['otp'] = otp
                        text = 'T2T Hi ' + str(user.first_name) + ', Please use OTP ' + str(
                            otp) + ' to complete the registration process on travelchannels.in'
                        SMS(mobile, text)
                        print('-----------------------OTP--------------------------')
                        print(otp)
                        return redirect('core:booking-otp-verification')
                except:
                    messages.error(request, 'Invalid Credentials', extra_tags='alert alert-warning alert-dismissible')
                    return redirect('core:booking-login')
            elif type == 'register':
                try:
                    email = request.POST['email_id']
                    full_name = request.POST['full_name']
                    user = models.User.objects.create_user(username=mobile, email=email, password=password)
                    lname = ''
                    fname, lname = full_name.split()
                    user.first_name = fname
                    user.last_name = lname
                    user.mobile = mobile
                    user.save()
                    otp = random.randint(1000,9999)
                    request.session['mobile'] = mobile
                    request.session['password'] = password
                    request.session['otp'] = otp
                    text = 'T2T Hi '+ str(full_name) + ', Please use OTP ' + str(otp) + ' to complete the registration process on travelchannels.in'
                    SMS(mobile, text)
                    print('-----------------------OTP--------------------------')
                    print(otp)
                    customerprofile = customermodels.customerprofile.objects.create(user=user)
                    referal_code = customermodels.customer_promotional.objects.create(customer=customerprofile,
                                                                                      promotional_code=str(mobile),
                                                                                      referralbenefit=50,
                                                                                      customerbenefit=50,
                                                                                      is_activated=True)

                    return redirect('core:booking-otp-verification')
                except:
                    messages.error(request, 'User Already Exists', extra_tags='alert alert-warning alert-dismissible')
        return redirect('core:booking-login')

def OTPVerificationView(request):
    if request.method == 'POST':
        input_otp = request.POST['otp']
        generated_otp = request.session['otp']
        if int(input_otp) == int(generated_otp):
            mobile = request.session['mobile']
            password = request.session['password']
            user = authenticate(username=mobile, password=password)
            login(request, user)
            user.mobile_verified = True
            user.save()
            print('OTP VERIFIED', user.mobile_verified)
            return redirect('core:checkout')
        else:
            messages.error(request, 'Invalid OTP', extra_tags='alert alert-warning alert-dismissible')
            return redirect('core:booking-otp-verification')
    else:
        ride_type = request.session['ride_type']
        pickup_city = request.session['pickup_city']
        drop_city = request.session['drop_city']
        pickup = request.session['pickup']
        drop = request.session['drop']
        pickup_datetime = request.session['pickup_datetime']
        drop_datetime = request.session['drop_datetime']
        duration = request.session['duration']
        distance = request.session['distance']
        car_type = request.session['car_type']
        ride_checkboxes = request.session['ride_checkboxes']
        ride_total = request.session['ride_total']
        distance_text = request.session['distance_text']
        duration_text = request.session['duration_text']
        mobile = request.session['mobile']
        pickup_datetime = dateutil.parser.parse(pickup_datetime)
        drop_datetime = dateutil.parser.parse(drop_datetime)
        context = {
            'ride_type': ride_type,
            'pickup_city': pickup_city,
            'drop_city': drop_city,
            'pickup': pickup,
            'drop': drop,
            'pickup_datetime': pickup_datetime,
            'drop_datetime': drop_datetime,
            'duration': duration,
            'distance': distance,
            'car_type': car_type,
            'ride_checkboxes': ride_checkboxes,
            'ride_total': ride_total,
            'distance_text': distance_text,
            'duration_text': duration_text,
            'mobile': mobile,
        }
        return render(request, 'customer_otp_verification.html', context)

def CheckoutView(request):
    if request.method == 'POST':
        type = request.POST['type']
        if type == 'coupon':
            coupon_code = request.POST['coupon_code']
            try:
                coupon_code_qs = customermodels.customer_promotional.objects.filter(promotional_code=coupon_code, is_activated=True)[0]
                print(coupon_code_qs)
                request.session['coupon_code_id'] = coupon_code_qs.id
                print(coupon_code_qs.id)
                ride_total = request.session['ride_total']
                print(ride_total)
                final_ride_fair = ride_total - coupon_code_qs.customerbenefit
                request.session['final_ride_fair'] = final_ride_fair
                print('--------------------COUPON----------------------')
                print(final_ride_fair)
            except:
                messages.error(request, 'Invalid Coupon', extra_tags='alert alert-warning alert-dismissible')
        elif type == 'details':
            if 'name' in request.POST:
                name = request.POST['name']
            else:
                name = request.user.get_full_name()
            if 'mobile' in request.POST:
                mobile = request.POST['mobile']
            else:
                mobile = request.user.mobile
            pickup_location = request.POST['pickup_location']
            drop_location = request.POST['drop_location']
            request.session['name'] = name
            request.session['mobile'] = mobile
            request.session['pickup_location'] = pickup_location
            request.session['drop_location'] = drop_location
            print(name, mobile)
            return redirect('core:payment')
        return redirect('core:checkout')
    else:
        ride_type = request.session['ride_type']
        pickup_city = request.session['pickup_city']
        drop_city = request.session['drop_city']
        pickup = request.session['pickup']
        drop = request.session['drop']
        pickup_datetime = request.session['pickup_datetime']
        drop_datetime = request.session['drop_datetime']
        duration = request.session['duration']
        distance = request.session['distance']
        car_type = request.session['car_type']
        ride_checkboxes = request.session['ride_checkboxes']
        ride_total = request.session['ride_total']
        distance_text = request.session['distance_text']
        duration_text = request.session['duration_text']

        final_prices = request.session['final_prices']
        price_km = request.session['price_km']
        initial_charges = request.session['initial_charges']
        additional_charges = request.session['additional_charges']
        early_pickup_charges = request.session['early_pickup_charges']
        late_drop_charges = request.session['late_drop_charges']
        night_charges = request.session['night_charges']
        driver_allowances = early_pickup_charges + late_drop_charges + night_charges
        gst_charges = request.session['gst_charges']

        pickup_datetime = dateutil.parser.parse(pickup_datetime)
        drop_datetime = dateutil.parser.parse(drop_datetime)

        final_ride_fair = ride_total
        coupon_code = ''
        if 'coupon_code_id' in request.session:
            coupon_code_id = request.session['coupon_code_id']
            coupon_code = customermodels.customer_promotional.objects.get(id=int(coupon_code_id))
            final_ride_fair = ride_total - coupon_code.customerbenefit
            coupon_code = coupon_code.promotional_code

        checkbox_charges = 0
        if 'ride_checkboxes' in request.session:
            ride_checkboxes = request.session['ride_checkboxes']
            for checkbox_id in ride_checkboxes:
                checkbox_charge = int(models.ride_choices.objects.get(id=checkbox_id).value)
                print(checkbox_charge)
                checkbox_charges += checkbox_charge

        request.session['final_ride_fair'] = final_ride_fair
        advance = int(ride_total*0.15)

        ride_type_qs = models.ride_types.objects.get(name=ride_type)
        ride_checkboxes_qs = models.ride_choices.objects.filter(ride_type__in=[ride_type_qs])
        context = {
            'ride_type': ride_type,
            'pickup_city': pickup_city,
            'drop_city': drop_city,
            'pickup': pickup,
            'drop': drop,
            'pickup_datetime': pickup_datetime,
            'drop_datetime': drop_datetime,
            'duration': duration,
            'distance': distance,
            'car_type': car_type,
            'ride_checkboxes': ride_checkboxes,
            'ride_total': ride_total,
            'distance_text': distance_text,
            'duration_text': duration_text,
            'advance': advance,
            'final_ride_fair':final_ride_fair,
            'coupon_code':coupon_code,

            'initial_charges':initial_charges,
            'additional_charges':additional_charges,
            'early_pickup_charges':early_pickup_charges,
            'late_drop_charges':late_drop_charges,
            'night_charges':night_charges,
            'driver_allowances':driver_allowances,
            'checkbox_charges':checkbox_charges,
            'gst_charges':gst_charges,
            'ride_checkboxes_qs':ride_checkboxes_qs,
        }
        return render(request, 'customer_ride_checkout.html', context)

def PaymentView(request):
    print('--------------------PAYMENT VIEW ----------------------------')
    ride_type = request.session['ride_type']
    pickup_city = request.session['pickup_city']
    drop_city = request.session['drop_city']
    pickup = request.session['pickup']
    drop = request.session['drop']
    pickup_datetime = request.session['pickup_datetime']
    drop_datetime = request.session['drop_datetime']
    duration = request.session['duration']
    distance = request.session['distance']
    car_type = request.session['car_type']
    ride_checkboxes = request.session['ride_checkboxes']
    ride_total = request.session['ride_total']
    distance_text = request.session['distance_text']
    duration_text = request.session['duration_text']

    final_ride_fair = request.session['final_ride_fair']
    ride_total = request.session['ride_total']
    price_km = request.session['price_km']
    initial_charges = request.session['initial_charges']
    additional_charges = request.session['additional_charges']

    early_pickup_charges = request.session['early_pickup_charges']
    late_drop_charges = request.session['late_drop_charges']
    night_charges = request.session['night_charges']
    driver_allowances = early_pickup_charges + late_drop_charges + night_charges

    gst_charges = request.session['gst_charges']
    advance = int(final_ride_fair * 0.15)

    name = request.session['name']
    mobile = request.session['mobile']
    pickup_location = request.session['pickup_location']
    drop_location = request.session['drop_location']

    ride_type_qs = models.ride_types.objects.filter(name__icontains = ride_type)[0]
    car_type_qs = models.car_types.objects.filter(name__icontains = car_type)[0]

    coupon_qs = None
    if 'coupon_code_id' in request.session:
        coupon_code_id = request.session['coupon_code_id']
        coupon_qs = customermodels.customer_promotional.objects.get(id = coupon_code_id)

    pickup_city = models.city.objects.get(name=pickup_city)
    drop_city = models.city.objects.get(name=drop_city)
    booking = models.ride_booking.objects.create(
        user = request.user,
        name = name,
        phone_no = mobile,

        ride_type = ride_type_qs,
        car_type = car_type_qs,
        pickup_city = pickup_city,
        drop_city = drop_city,
        pickup=pickup,
        drop=drop,
        distance = distance,
        duration = duration,

        booking_datetime=datetime.datetime.now(),
        pickup_datetime = pickup_datetime,
        drop_datetime = drop_datetime,
        exact_pickup =pickup_location,
        exact_drop = drop_location,

        initial_charges = initial_charges,
        additional_charges =additional_charges,
        early_pickup_charges =early_pickup_charges,
        late_drop_charges =late_drop_charges,
        night_charges =night_charges,
        gst_charges =gst_charges,
        final_fare =ride_total,

        coupon=coupon_qs,
        balance_used=0,

        final_ride_fare =final_ride_fair,
        advance =advance,
        ride_status='Cancelled'
    )

    if 'ride_checkboxes' in request.session:
        ride_checkboxes = request.session['ride_checkboxes']
        for checkbox_id in ride_checkboxes:
            choice = models.ride_choices.objects.get(id=checkbox_id)
            booking.additional_choices.add(choice)
            booking.save()

    data = {
        'txnid': payu.generate_txnid(), 'amount': str(int(advance)), 'productinfo': str(ride_type),
        'firstname': str(request.user.first_name), 'email': str(request.user.email), 'udf1': str(booking.id),
    }
    print(data)
    payu_data = payu.initiate_transaction(data)
    print('--------------------PAYMENT VIEW Rendering ----------------------------')
    return render(request, 'payments/payu_checkout.html', {"posted": payu_data})

def checkout2(request):
    hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    MERCHANT_KEY = "8n6elxOQ"
    key = "8n6elxOQ"
    SALT = "B5Uh58bhu5"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    action = ''
    posted = {}
    # Merchant Key and Salt provided y the PayU.
    for i in request.POST:
        posted[i] = request.POST[i]
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid = hash_object.hexdigest()[0:20]
    hashh = ''
    posted['txnid'] = txnid
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key'] = key
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    hashh = hashlib.sha512(hash_string).hexdigest().lower().encode('utf-8')
    action = PAYU_BASE_URL

    if (posted.get("key") != None and posted.get("txnid") != None and posted.get(
            "productinfo") != None and posted.get("firstname") != None and posted.get("email") != None):
        return render_to_response('current_datetime.html', RequestContext(request,
                                                                          {"posted": posted, "hashh": hashh,
                                                                           "MERCHANT_KEY": MERCHANT_KEY,
                                                                           "txnid": txnid,
                                                                           "hash_string": hash_string,
                                                                           "action": "https://test.payu.in/_payment"}))
    else:
        return render_to_response('current_datetime.html', RequestContext(request,
                                                                          {"posted": posted, "hashh": hashh,
                                                                           "MERCHANT_KEY": MERCHANT_KEY,
                                                                           "txnid": txnid,
                                                                           "hash_string": hash_string,
                                                                           "action": "."}))

# Payu success return page
@csrf_protect
@csrf_exempt
def payu_success(request):
    data = dict(zip(request.POST.keys(), request.POST.values()))
    response = payu.check_hash(data)
    data = response['data']
    booking_id = data['udf1']
    booking_qs = models.ride_booking.objects.get(id=booking_id)
    booking_qs.advance_payment_received = True
    booking_qs.ride_status = 'Booked'
    booking_qs.save()
    amount = data['amount']
    txn_id = data['txnid']
    mode = data['mode']
    payment = models.payment.objects.create(booking_id = booking_id, amount=amount, txn_id=txn_id, mode=mode)
    payment.save()
    message = 'Your Ride is Successfully Booked (Booking ID: T2T-' + booking_id + ') You will receive the car and driver details shortly.'
    SMS(booking_qs.phone_no, message)
    context = response['data']
    context['booking'] = booking_qs
    return render(request, 'payments/payment_success.html', context)

# Payu failure page
@csrf_protect
@csrf_exempt
def payu_failure(request):
    data = dict(zip(request.POST.keys(), request.POST.values()))
    response = payu.check_hash(data)
    context = response['data']
    return render(request, 'payments/payu_success.html', context)

def populate_data(request):
    cities = models.city.objects.all()
    car_types = models.car_types.objects.all()
    cal_attr = models.calc_attr.objects.all()

    for pickup_cities in cities:
        if pickup_cities.pickup:
            for dropcities in cities:
                if dropcities.drop:
                    for type in car_types:
                        for attr in cal_attr:
                            if attr.active:
                                try:
                                    new = models.calc_city_attr_value.objects.get(city1=pickup_cities,
                                                                                     city2=dropcities, car_type=type,
                                                                                     attr=attr)
                                except:
                                    new = models.calc_city_attr_value.objects.create(city1=pickup_cities,
                                                                                     city2=dropcities, car_type=type,
                                                                                     attr=attr, value=attr.value)
                                    new.save()
    return HttpResponse('Done')