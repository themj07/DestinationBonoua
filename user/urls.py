from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('reset_password/', views.password_reset_request, name='reset_password'),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    # path('forgot/', views.forgot, name='forgot'),
    # path('verify_forgot/', views.verify_forgot, name='verify_forgot'),
    # path('verify_otp/', views.verify_otp, name='verify_otp'),
    # path('verify_otp_login/', views.verify_otp_login, name='verify_otp_login'),
]