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
    path('booking-bid/', views.VendorBookingBidView, name='booking_vendor_bid'),

    path('assignments/', views.AssignmentsView, name='assignments'),
    path('assign-car-driver/<int:id>/', views.AssignCarDriverView, name='assign_car_driver'),
    path('reject/<int:id>/', views.RejectBookingView, name='reject_assignment'),

    path('ride-detail/', views.RideDetailsView, name='booking_detail'),
    path('ride-detail/start/<int:id>/', views.StartRideView, name='start_ride'),
    path('ride-detail/end/<int:id>/', views.EndRideView, name='end_ride'),
]
