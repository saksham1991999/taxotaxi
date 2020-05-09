from django import template
from core import models

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
