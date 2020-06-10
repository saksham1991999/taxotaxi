from django.urls import path
from . import views
app_name = 'vendor'

urlpatterns = [
    path('', views.DashboardView, name='dashboard'),
    path('register/', views.VendorRegistrationView, name='registration'),
    path('cara/', views.CarsView, name='cars'),
    path('drivers/', views.DriversView, name='drivers'),
    path('payments/', views.PaymentsView, name='payments'),
    path('booking-history/', views.BookingsHistoryView, name='booking_history'),
    path('bookings/', views.BookingsView, name='bookings'),
    path('assignments/', views.AssignmentsView, name='assignments'),
    path('ride/<int:id>/', views.RideDetailsView, name='booking'),
]
