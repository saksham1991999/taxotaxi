from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path('', views.HomeView, name='home'),

    # Main Page Urls
    path('general/', views.GeneralModelsView, name='general'),
    path('cities/update/', views.UpdateCityView, name='cities_update'),
    path('testimonial/add/', views.AddTestimonialView, name='testimonial_add'),
    path('testimonial/edit/<int:id>/', views.EditTestimonialView, name='testimonial_edit'),
    path('testimonial/delete/<int:id>/', views.DeleteTestimonialView, name='testimonial_delete'),
    path('home-page-banners/add/', views.AddMainPageBannersView, name='banner_add'),
    path('home-page-banners/edit/<int:id>/', views.EditMainPageBannersView, name='banner_edit'),
    path('home-page-banners/delete/<int:id>/', views.DeleteMainPageBannersView, name='banner_delete'),
    path('update-faqs/', views.UpdateFAQsView, name='update_faqs'),
    path('update-t&c/', views.UpdateTermsAndConditionsView, name='update_tnc'),

    path('contact-us/', views.ContactUsView, name='contact_us'),
    path('payments/', views.PaymentsView, name='payments'),

    # Ride Bookings Urls
    path('cancelled-rides/', views.CancelledRidesView, name='cancelled_rides'),
    path('booked-rides/', views.BookedRidesView, name='booked_rides'),
    path('assign-vendor-rides/', views.AssignVendorRidesView, name='assign_vendor_rides'),
    path('upcoming-rides/', views.UpcomingRidesView, name='upcoming_rides'),
    path('ongoing-rides/', views.OngoingRidesView, name='ongoing_rides'),
    path('completed-rides/', views.CompletedRidesView, name='completed_rides'),
    path('user-cancelled-rides/', views.UserCancelledRides, name='user_cancelled_rides'),
    path('vendor-cancelled-rides/', views.UserCancelledRides, name='vendor_cancelled_rides'),

    path('assign-vendors/<int:id>/', views.AssignVendorsView, name='assign_vendors'),
    path('vendor-bids/<int:id>/', views.UpdateVendorBidsView, name='vendor_bids'),
    path('assign-final-vendor/<int:id>/', views.AssignFinalVendorView, name='assign_final_vendor'),
    path('assign-driver-car/<int:id>/', views.AssignDriverCarView, name='assign_driver_car'),
    path('start-ride/<int:id>/', views.StartRideView, name='start_ride'),
    path('end-ride/<int:id>/', views.EndRideView, name='end_ride'),
    path('verify-ride/<int:id>/', views.VerifyRideView, name='verify_ride'),

    path('final-ride-details/', views.FinalRideDetailsView, name='final_ride_details'),

    # Popular Destinations Urls
    path('popular-destinations/', views.PopularDestinationsView, name = 'popular_destinations'),
    path('popular-destinations/add/', views.AddPopularDestinationView, name = 'popular_destinations_add'),
    path('popular-destinations/edit/<int:id>/', views.EditPopularDestinationView, name = 'popular_destinations_edit'),
    path('popular-destinations/delete/<int:id>/', views.DeletePopularDestinationView, name = 'popular_destinations_delete'),

    # Car Type Urls
    path('car-type/', views.CarTypePageViews, name='car_type'),
    path('update-car-attributes/', views.UpdateCarAttributes, name='update_car_attributes'),
    path('update-car-attribute-values/', views.UpdateCarAttributeValueView, name='update_car_attribute_values'),
    path('update-ride-additional-choices/', views.UpdateRideAdditionalChoices, name='update_ride_additional_choices'),
    path('update-city-ride-attributes/', views.UpdateCityRideAttributeValues, name='update_city_ride_attributes'),

    # Blog Urls
    path('blogs/',views.BlogsView, name="blogs"),
    path('update-categories/', views.UpdateBlogCategoriesView, name="update_categories"),
    path('post/add/',views.AddBlogPostView, name="post_add"),
    path('post/edit/<int:id>/',views.EditBlogPostView, name="post_edit"),
    path('post/delete/<int:id>/',views.DeleteBlogPostView, name="post_delete"),
    path('post/delete-comment/<int:id>/',views.DeleteBlogPostCommentView, name="post_comment_delete"),

    # Customer Urls
    path('customers/',views.CustomersView, name="customers"),
    path('customers/add/',views.AddCustomerView, name="customer_add"),
    path('customers/edit/<int:id>/',views.EditCustomerView, name="customer_edit"),
    path('customers/delete/<int:id>/',views.DeleteCustomerView, name="customer_delete"),

    path('promotional/update/<int:id>/', views.UpdateCustomerPromotionalView, name="customer_update_promotional"),

    # Vendor Urls
    path('vendors/',views.VendorsView, name="vendors"),
    path('vendor/<int:id>/',views.VendorView, name="vendor"),
    path('vendor/add/',views.VendorsView, name="vendor_add"),
    path('vendor/update-status/<int:id>/',views.UpdateVendorStatusView, name="vendor_update_status"),
    path('vendor/edit/<int:id>/',views.EditVendorView, name="vendor_edit"),
    path('vendor/delete/<int:id>/',views.DeleteVendorView, name="vendor_delete"),
    # path('vendor/cars/update/<int:id>/', views.UpdateVendorCarsView, name="vendor_cars_update"),
    # path('vendor/drivers/update/<int:id>/', views.UpdateVendorDriversView, name="vendor_drivers_update"),
    path('vendor/bank-details/update/<int:id>/', views.UpdateVendorBankDetailsView, name="vendor_banks_update"),
    path('vendor/car/add/<int:id>/', views.AddVendorCarView, name="vendor_car_add"),
    path('vendor/car/edit/<int:id>/', views.EditVendorCarView, name="vendor_car_edit"),
    path('vendor/car/delete/<int:id>/', views.DeleteVendorCarView, name="vendor_car_delete"),
    path('vendor/driver/add/<int:id>/', views.AddVendorDriver, name="vendor_driver_add"),
    path('vendor/driver/edit/<int:id>/', views.EditVendorDriver, name="vendor_driver_edit"),
    path('vendor/driver/delete/<int:id>/', views.DeleteVendorDriver, name="vendor_driver_delete"),

    # Test Views
    path('test/1/', views.TestView1, name='test1'),
    path('test/2/', views.TestView2, name='test2'),
    path('test/3/', views.TestView3, name='test3'),
    path('test/4/', views.TestView4, name='test4'),
    path('test/5/', views.TestView5, name='test5'),
    path('dashboard/', views.DashboardView , name='dashboard'),
    path('assign-vendors/<int:id>/', views.AssignVendorsView , name='assign_vendor'),
    path('assign-final-vendor/<int:id>/', views.AssignFinalVendorView , name='assign_final_vendor'),
]
