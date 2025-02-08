from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('404/', views.error_404, name='404'),
    path('hotel/', views.hotel, name='hotel'),
    path('hotel-single/', views.hotel_single, name='hotel-single'),
    path('places/', views.places, name='places'),
    path('places-single/', views.places_single, name='places-single'),
    path('service/', views.service, name='service'),
    path('service-s2/', views.service_s2, name='service-s2'),
    path('service-single/', views.service_single, name='service-single'),
]