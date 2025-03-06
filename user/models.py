from django.db import models



# models.py

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)  # L'email doit être unique
    date_subscribed = models.DateTimeField(auto_now_add=True)  # Date d'inscription

    def __str__(self):
        return self.email