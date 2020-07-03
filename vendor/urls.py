from django.urls import path
from . import views
app_name = 'vendor'

urlpatterns = [
    path('', views.DashboardView, name='dashboard'),
    path('register/', views.VendorRegistrationView, name='registration'),
    path('cars/', views.CarsView, name='cars'),
    path('cars/edit/<int:id>/', views.EditCarView, name='edit_car'),
    path('cars/delete/<int:id>/', views.DeleteCarView, name='delete_car'),
    path('drivers/', views.DriversView, name='drivers'),
    path('drivers/edit/<int:id>/', views.EditDriverView, name='edit_driver'),
    path('drivers/delete/<int:id>/', views.DeleteDriverView, name='delete_driver'),


    path('payments/', views.PaymentsView, name='payments'),
    path('booking-history/', views.BookingsHistoryView, name='booking_history'),
    path('bookings/', views.BookingsView, name='bookings'),
    path('assignments/', views.AssignmentsView, name='assignments'),
    path('ride/<int:id>/', views.RideDetailsView, name='booking_detail'),
]
