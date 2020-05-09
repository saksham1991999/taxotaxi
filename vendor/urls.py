from django.urls import path
from . import views
app_name = 'vendor'

urlpatterns = [
    path('', views.DashboardView, name='dashboard'),
    path('register/', views.VendorRegistrationView, name='registration'),
]
