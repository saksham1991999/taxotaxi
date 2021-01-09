
from django.urls import path
from . import views
app_name = 'customer'

urlpatterns = [
    path('', views.DashboardView, name='dashboard'),
    path('cancel-ride/<int:id>/', views.CancelRideView, name='cancel_ride'),
    path('complete-payment/<int:id>/', views.CompletePayment, name='complete_payment'),
]
