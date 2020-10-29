from django import template
from core import models
from vendor import models as vendormodels
register = template.Library()


@register.filter
def attr_value(type, attr):
    attr = models.car_attr.objects.get(name=attr)
    try:
        if attr.name == "Price per Km":
            return 'price_km' + str(type.id)
        else:
            value = models.car_attr_comparison.objects.get(car_type=type, attr_name=attr).value
            return value
    except:
        return ' '

@register.filter
def price_km(value, final_prices):
    if 'price_km' in value:
        id = int(value[-1])-1
        return int(final_prices[id])
    else:
        return value


@register.filter
def final_price_type(final_prices, type):
    id = type.id
    try:
        return int(final_prices[id-1])
    except:
        return ' '

@register.filter
def car_type_image(type):
    try:
        return type.image.url
    except:
        return ' '

@register.filter
def ride_choice_value(choice_id):
    pass

@register.filter
def adder(var1, var2):
    ans = int(var1) + int(var2)
    return ans

@register.filter
def car_attr_value(type, attr):
    attr = models.car_attr.objects.get(name=attr)
    try:
        value = models.car_attr_comparison.objects.get(car_type=type, attr_name=attr).value
        return value
    except:
        return ' '


@register.filter
def profile_pic(user):
    if user.is_authenticated:
        pic = None
        if user.is_vendor:
            vendor = vendormodels.vendorprofile.objects.get(user = user)
            if vendor.image:
                pic = vendor.image.url
        elif user.is_driver:
            driver = vendormodels.driver.objects.get(user = user)
            if driver.image:
                pic = driver.image.url
        else:
            if user.profile_pic:
                pic = user.profile_pic.url
        if pic:
            return pic
    return None

@register.filter
def first_name(user):
    if user.is_authenticated:
        if user.is_vendor:
            vendor = vendormodels.vendorprofile.objects.get(user = user)
            first_name = list(vendor.full_name.split())[0]
        elif user.is_driver:
            driver = vendormodels.driver.objects.get(user = user)
            first_name = list(driver.full_name.split())[0]
        else:
            first_name = user.first_name
        if first_name:
            return first_name
    return 'Guest'

@register.filter
def full_name(user):
    if user.is_authenticated:
        full_name = "Guest  "
        if user.is_vendor:
            vendor = vendormodels.vendorprofile.objects.get(user = user)
            if len(list(vendor.full_name.split())) > 1:
                full_name = vendor.full_name
            else:
                full_name = vendor.full_name + '  '
        elif user.is_driver:
            driver = vendormodels.driver.objects.get(user = user)
            if len(list(driver.full_name.split())) > 1:
                full_name = driver.full_name
            else:
                full_name = driver.full_name + '  '
        else:
            if user.first_name or user.last_name:
                full_name = str(user.first_name) + ' ' + str(user.last_name)

        if full_name:
            return full_name
    return 'Taxo Taxi'


@register.filter
def latest_bid(user, booking):
    bids = models.vendorbids.objects.filter(booking = booking, vendor__user = user).order_by('-datetime')
    if bids.exists():
        latest_bid_qs = bids[0]
        return int(latest_bid_qs.bid)
    else:
        return None