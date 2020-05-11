from django.urls import path
from . import views
app_name = 'core'

urlpatterns = [
    path('', views.HomeView, name='home'),

    path('coming-soon', views.ComingSoonView, name='coming_soon'),
    path('test/', views.TestView, name='test'),
    path('cars/', views.CarSpecificationsView, name='cars'),
    path('checkbox-adder/', views.CheckBoxesAdder, name='checkbox-adder'),
    

    path('faq/', views.FAQView, name='faq'),
    path('contact-us/', views.ContactView, name='contact'),

    path('login/', views.LoginView, name='login'),
    path('register/otp-verification', views.RegisterOTPVerification, name='register_otp_verification'),
    path('logout/', views.LogoutView, name='logout'),

    path('dashboard/', views.DashboardView, name='dashboard'),

    path('pickuplocations/', views.pickuplocations, name='pickup'),
    path('populatedata/', views.populate_data, name='populatedata'),

    path('booking/login/', views.CustomerLoginView, name='booking-login'),
    path('booking/authentication/', views.CustomerAuthenticationView, name='booking-authentication'),
    path('booking/otp-verification/', views.OTPVerificationView, name='booking-otp-verification'),
    path('checkout/', views.CheckoutView, name='checkout'),
    path('checkout2/', views.checkout2, name='checkout2'),
    path('payment/', views.PaymentView, name='payment'),
    path('payu/success', views.payu_success, name='payu_success'),
    path('payu/failure', views.payu_failure, name='payu_failure'),
]
