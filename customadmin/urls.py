from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path('', views.HomeView, name='home'),

    path('blogs/',views.BlogsView, name="blogs"),

    path('test/1/', views.TestView1, name='test1'),
    path('test/2/', views.TestView2, name='test2'),
    path('test/3/', views.TestView3, name='test3'),
    path('test/4/', views.TestView4, name='test4'),
    path('test/5/', views.TestView5, name='test5'),
    path('dashboard/', views.DashboardView , name='dashboard'),
    path('assign-vendors/<int:id>/', views.AssignVendorsView , name='assign_vendor'),
    path('assign-final-vendor/<int:id>/', views.AssignFinalVendorView , name='assign_final_vendor'),
]
