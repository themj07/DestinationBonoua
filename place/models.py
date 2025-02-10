from django.db import models

# Create your models here.


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
    

class ImageDefaultPlaceHolder(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='DefaultPlaceHolder/', blank=True, null=True)

    def __str__(self):
        return self.name
