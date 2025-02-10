from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('404/', views.error_404, name='404'),
    path('hotel/', views.hotel, name='hotel'),
    path('instituts/', views.instituts, name='instituts'),
    path('hotel-single/', views.hotel_single, name='hotel-single'),
    path('placesInstituts/', views.places_instituts, name='places-instituts'),
    path('placesTourismes/', views.places_tourismes, name='places-tourismes'),
    path('places-single-institut/', views.places_single_institut, name='places-single-institut'),
    path('places-single-tourisme/', views.places_single_tourisme, name='places-single-tourisme'),
    path('service/', views.service, name='service'),
    path('service-s2/', views.service_s2, name='service-s2'),
    path('service-single/', views.service_single, name='service-single'),
]