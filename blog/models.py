from django.db import models
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.



class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')  # Image principale
    image_1 = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # Image additionnelle 1
    image_2 = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # Image additionnelle 2
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Générer un slug automatiquement
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    blog = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"




class Contact(models.Model):
    SERVICE_CHOICES = [
        ('Institutions & Departements', 'Institutions & Departements'),
        ('Hotels', 'Hotels'),
        ('Autres', 'Autres'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ Utilisateur optionnel
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255, choices=SERVICE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.name} - {self.subject}"
