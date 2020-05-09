from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path('dashboard/', views.DashboardView , name='dashboard'),
    path('assign-vendors/<int:id>/', views.AssignVendorsView , name='assign_vendor'),
    path('assign-final-vendor/<int:id>/', views.AssignFinalVendorView , name='assign_final_vendor'),
]
