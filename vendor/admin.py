from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.vendorprofile)
admin.site.register(models.vendor_cars)
admin.site.register(models.driver)
admin.site.register(models.bank_detail)