from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path('', views.HomeView, name='home'),

    # Main Page Urls
    path('general/', views.GeneralModelsView, name='general'),

    path('city/add/', views.AddCityView, name='city_add'),
    path('city/edit/<int:id>/', views.EditCityView, name='city_edit'),
    path('city/delete/<int:id>/', views.DeleteCityView, name='city_delete'),

    path('testimonial/add/', views.AddTestimonialView, name='testimonial_add'),
    path('testimonial/edit/<int:id>/', views.EditTestimonialView, name='testimonial_edit'),
    path('testimonial/delete/<int:id>/', views.DeleteTestimonialView, name='testimonial_delete'),

    path('home-page-banners/add/', views.AddMainPageBannersView, name='banner_add'),
    path('home-page-banners/edit/<int:id>/', views.EditMainPageBannersView, name='banner_edit'),
    path('home-page-banners/delete/<int:id>/', views.DeleteMainPageBannersView, name='banner_delete'),

    path('update-faqs/', views.UpdateFAQsView, name='update_faqs'),
    path('contact-us/', views.ContactUsView, name='contact_us'),

    # Blog Urls
    path('blogs/',views.BlogsView, name="blogs"),
    path('update-categories/', views.UpdateBlogCategoriesView, name="update_categories"),
    path('post/add/',views.AddBlogPostView, name="post_add"),
    path('post/edit/<int:id>/',views.EditBlogPostView, name="post_delete"),
    path('post/delete/<int:id>/',views.DeleteBlogPostView, name="post_delete"),

    # Customer Urls
    path('customers/',views.CustomersView, name="customers"),
    path('customers/add/',views.AddCustomerView, name="customer_add"),
    path('customers/edit/<int:id>/',views.EditCustomerView, name="customer_edit"),
    path('customers/delete/<int:id>/',views.DeleteCustomerView, name="customer_delete"),
    path('customers/promotional/update/<int:id>/', views.UpdateCustomerPromotionalView, name="customer_update_promotional"),

    # Vendor Urls
    path('vendors/',views.VendorsView, name="vendors"),
    path('vendor/add/',views.VendorsView, name="vendor_add"),
    path('vendor/edit/<int:id>/',views.EditVendorView, name="vendor_edit"),
    path('vendor/delete/<int:id>/',views.DeleteVendorView, name="vendor_delete"),

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
