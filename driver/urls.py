from django.urls import path
from . import views
app_name = 'driver'

urlpatterns = [
    path('', views.DashboardView, name='dashboard'),

    path('upcoming/', views.UpcomingRidesView, name='upcoming'),
    path('payments/', views.PaymentsView, name='payments'),
    path('booking-history/', views.BookingsHistoryView, name='booking_history'),

    path('ride-detail/', views.RideDetailsView, name='booking_detail'),
    path('ride-detail/start/<int:id>/', views.StartRideView, name='start_ride'),
    path('ride-detail/end/<int:id>/', views.EndRideView, name='end_ride'),
]
