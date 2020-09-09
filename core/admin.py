from django.contrib import admin
from . import models
# Register your models here.
admin.site.site_header = 'TaxoTaxi'
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class CalCityAttrValueResource(resources.ModelResource):

    class Meta:
        model = models.calc_city_attr_value
        fields = ('id', 'city1__name', 'city1', 'city2__name', 'city2', 'car_type__name', 'car_type', 'attr__name', 'attr', 'value')
        export_order = ('id', 'city1__name', 'city1', 'city2__name', 'city2', 'car_type__name', 'car_type', 'attr__name', 'attr', 'value')

class FinalRideResource(resources.ModelResource):

    class Meta:
        model = models.final_ride_detail
        fields = (
            "booking__name",
            "booking__phone_no",
            "booking__ride_type__name",
            "booking__car_type__name",
            "booking__pickup_city__name",
            "booking__pickup",
            "booking__exact_pickup",
            "booking__drop_city__name",
            "booking__drop",
            "booking__exact_drop",
            "booking__price_km",
            "booking__booking_datetime",

            "booking__initial_charges",
            "booking__additional_charges",
            "booking__early_pickup_charges",
            "booking__late_drop_charges",
            "booking__night_charges",
            "booking__gst_charges",
            "booking__final_fare",
            "booking__coupon__promotional_code",
            "booking__balance_used",
            "booking__balance_used",
            "booking__final_ride_fare",
            "booking__advance",

            "bid__vendor__full_name",
            "bid__vendor__contact1",
            "bid__bid",
            "driver__full_name",
            "driver__contact1",
            "car__car_type",
            "car__registration_no",

            "initial_odometer_reading",
            "final_odometer_reading",

            "get_total_distance",
            "get_extra_km",
            "get_extra_km_price",
            "get_total_extra_charges",
            "get_total_extra_gst",
            "get_total_extra_charges_with_gst",
            "get_final_ride_charges",


            "other_charges",
            "collected_amount",

            "start_datetime",
            "end_datetime",
            "rating",
            "review",
        )




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
    resource_class = CalCityAttrValueResource

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

class BookingAdmin(ImportExportModelAdmin):
    list_display = [
                    'id',
                    'name',
                    'ride_type',
                    'car_type',
                    'ride_status',
                    'final_ride_fare',
                    ]
    list_display_links = [
                    'name',
                    ]
    list_filter = [
                    'ride_status',
                    ]
    search_fields = [
                    'name',
                    ]

class faq_admin(ImportExportModelAdmin):
    pass

class terms_and_conditions_admin(ImportExportModelAdmin):
    pass

class PaymentAdmin(ImportExportModelAdmin):
    list_display = [
                    'id',
                    'booking',
                    'txn_id',
                    'datetime',
                    'amount',
                    'mode',
                    ]
    list_display_links = [
                    'id',
                    'booking',
                    'txn_id',
                    'datetime',
                    ]
    list_filter = [
                    'datetime',
                    'mode',
                    ]
    search_fields = [
                    'booking',
                    'txn_id',
                    'datetime',
                    'amount',
                    'mode',
                    ]

class FinalRideDetail(ImportExportModelAdmin):
    resource_class = FinalRideResource

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

admin.site.register(models.ride_booking, BookingAdmin)
admin.site.register(models.payment)
admin.site.register(models.assign_vendor)
admin.site.register(models.vendorbids)
admin.site.register(models.final_ride_detail, FinalRideDetail)