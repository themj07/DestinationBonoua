from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('404/', views.error_404, name='404'),
    path('hotel/<int:type_id>/', views.hotel, name='hotel'),
    path('hotel-single/<int:tourisme_id>/', views.hotel_single, name='hotel-single'),
    path('placesInstituts/', views.places_instituts, name='placesInstituts'),
    path('instituts/<int:type_id>/', views.instituts, name='instituts'),
    path('places-single-institut/<int:institution_id>/', views.places_single_institut, name='places-single-institut'),
    path('placesTourismes/', views.places_tourismes, name='places-tourismes'),
]