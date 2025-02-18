from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('forgot/', views.forgot, name='forgot'),
    path('login/', views.user_login, name='login'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('verify_otp_login/', views.verify_otp_login, name='verify_otp_login'),

]