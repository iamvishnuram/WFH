from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('kaseyaWFH-admin/logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('get_employee_details/', views.get_employee_details, name='get_employee_details'),
    path('get_authenticated_employee_details/', views.get_authenticated_employee_details, name='get_authenticated_employee_details'),

]

