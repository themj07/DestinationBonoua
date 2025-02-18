# models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    def is_otp_expired(self):
        """Vérifie si l'OTP a expiré."""
        if self.otp_expiry is None:
            return True
        return timezone.now() > self.otp_expiry

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
