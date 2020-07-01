from django.contrib import admin
from . import models
# Register your models here.
admin.site.site_header = 'TaxoTaxi'
from import_export.admin import ImportExportModelAdmin

class car_attr_comparison_admin(ImportExportModelAdmin):
    list_display = [
                    'attr_name',
                    'car_type',
                    'value',
                    ]
    list_editable = [
                    'value',
                    ]
    list_display_links = [
                    'attr_name',
                    'car_type',
                    ]
    list_filter = [
                    'attr_name',
                    'car_type',
                    'value',
                    ]
    search_fields = [
                    'attr_name',
                    'car_type',
                    'value',
                    ]

class city_admin(ImportExportModelAdmin):
    list_display = [
                    'name',
                    'state',
                    'pickup',
                    'drop',
                    ]
    list_editable = [
                    'pickup',
                    'drop',
                    ]
    list_display_links = [
                    'name',
                    'state',
                    ]
    list_filter = [
                    'name',
                    'state',
                    'pickup',
                    'drop',
                    ]
    search_fields = [
                    'name',
                    'state',
                    'pickup',
                    'drop',
                    ]
class calc_city_attr_value_admin(ImportExportModelAdmin):
    list_display = [
                    'city1',
                    'city2',
                    'car_type',
                    'attr',
                    'value',
                    ]
    list_editable = [
                    'value',
                    ]
    list_display_links = [
                    'city1',
                    'city2',
                    'car_type',
                    'attr',
                    ]
    list_filter = [
                    'city1',
                    'city2',
                    'car_type',
                    'attr',
                    ]
    search_fields = [
                    'city1',
                    'city2',
                    'car_type',
                    'attr',
                    'value',
                    ]

class calc_attr_admin(ImportExportModelAdmin):
    list_display = [
                    'name',
                    'active',
                    'value',
                    'is_multiplied',
                    'is_time_dependent',
                    ]
    list_editable = [
                    'active',
                    'value',
                    'is_multiplied',
                    'is_time_dependent',
    ]
    list_display_links = [
                    'name',
                    ]
    list_filter = [
                    'name',
                    'active',
                    'value',
                    'is_multiplied',
                    'is_time_dependent',

                    ]
    search_fields = [
                    'name',
                    'active',
                    'value',
                    'is_multiplied',
                    'is_time_dependent',
                    ]

class ride_choices_admin(ImportExportModelAdmin):
    list_display = [
                    'name',
                    'value',
                    ]
    list_editable = [
                    'value',
                    ]
    list_display_links = [
                    'name',
                    ]
    list_filter = [
                    'name',
                    'value',
                    ]
    search_fields = [
                    'name',
                    'value',
                    ]

class banner_admin(ImportExportModelAdmin):
    list_display = [
                    'image',
                    'h2',
                    'h5',
                    ]
    list_display_links = [
                    'image',
                    'h2',
                    'h5',
                    ]
    list_filter = [
                    'image',
                    'h2',
                    'h5',
                    ]
    search_fields = [
                    'image',
                    'h2',
                    'h5',
                    ]

class expected_time_hault_admin(ImportExportModelAdmin):
    list_display = [
                    'ride_type',
                    'ride_time',
                    'hault_time',
                    ]
    list_editable = [
                    'ride_time',
                    'hault_time',
                    ]
    list_display_links = [
                    'ride_type',
                    ]
    list_filter = [
                    'ride_type',
                    ]
    search_fields = [
                    'ride_type',
                    ]

class ride_types_admin(ImportExportModelAdmin):
    list_display = [
                    'name',
                    'comment',
                    ]
    list_display_links = [
                    'name',
                    'comment',
                    ]
    list_filter = [
                    'name',
                    ]
    search_fields = [
                    'name',
                    'comment',
                    ]

class faq_admin(ImportExportModelAdmin):
    pass

class terms_and_conditions_admin(ImportExportModelAdmin):
    pass

admin.site.register(models.ride_types, ride_types_admin)
admin.site.register(models.User)
admin.site.register(models.user_referral)
admin.site.register(models.city, city_admin)

admin.site.register(models.location)
admin.site.register(models.airport)

admin.site.register(models.car_types)
admin.site.register(models.car_attr)
admin.site.register(models.car_attr_comparison, car_attr_comparison_admin)
admin.site.register(models.ride_choices, ride_choices_admin)


admin.site.register(models.banner, banner_admin)
admin.site.register(models.popular_destinations)
admin.site.register(models.calc_attr, calc_attr_admin)


admin.site.register(models.calc_city_attr_value, calc_city_attr_value_admin)
admin.site.register(models.testimonials)
admin.site.register(models.faq, faq_admin)
admin.site.register(models.TermsAndConditions, terms_and_conditions_admin)
admin.site.register(models.contact)
admin.site.register(models.ride_booking)
admin.site.register(models.final_ride_detail)