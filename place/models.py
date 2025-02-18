from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Create your models here.


class DefaultPlaceHolderPersonne(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='DefaultPlaceHolder/', blank=True, null=True)

    def __str__(self):
        return self.name


class InstitutionType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='institution_types/', blank=True, null=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(InstitutionType, on_delete=models.CASCADE)
    address = models.TextField()
    contact = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='institutions/', blank=True, null=True)  
    image_2 = models.ImageField(upload_to='institutions/extra_images/', blank=True, null=True)  
    image_3 = models.ImageField(upload_to='institutions/extra_images/', blank=True, null=True)  # Troisième image

    services_proposes = models.TextField(blank=True, null=True)  # Services proposés
    horaires_ouverture = models.TextField(blank=True, null=True)  # Horaires d'ouverture
    informations_stationnement = models.TextField(blank=True, null=True)  # Informations sur le stationnement
    autres_informations = models.TextField(blank=True, null=True)  # Autres informations


    def __str__(self):
        return self.name
    
    
class ToursismeType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='tourisme_types/', blank=True, null=True)

    def __str__(self):
        return self.name


class Toursisme(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ToursismeType, on_delete=models.CASCADE)
    address = models.TextField()
    prix_par_nuit = models.CharField(max_length=50, blank=True, null=True)
    note = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),  # Valeur minimale 0
            MaxValueValidator(5)   # Valeur maximale 5
        ],
        blank=True,
        null=True
    )
    contact = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='tourisme/', blank=True, null=True)  
    image_2 = models.ImageField(upload_to='tourisme/extra_images/', blank=True, null=True)  
    image_3 = models.ImageField(upload_to='tourisme/extra_images/', blank=True, null=True)  # Troisième image
    image_4 = models.ImageField(upload_to='tourisme/extra_images/', blank=True, null=True)  # Troisième image
    image_5 = models.ImageField(upload_to='tourisme/extra_images/', blank=True, null=True)  # Troisième image
    description = models.TextField(blank=True, null=True)

    equipements = models.TextField(blank=True, null=True)
    services = models.TextField(blank=True, null=True)



    def __str__(self):
        return self.name


# models.py

# models.py

class CommentaireTourisme(models.Model):
    tourisme = models.ForeignKey('Toursisme', on_delete=models.CASCADE, related_name="commentaires")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentaires", null=True, blank=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(default='', blank=True)
    note = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.user.username if self.user else self.nom} - {self.tourisme.name} ({self.note}⭐)"
