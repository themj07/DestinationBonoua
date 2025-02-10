from django.contrib import admin
from .models import Institution, InstitutionType, ImageDefaultPlaceHolder


# Register your models here.

admin.site.register(Institution)
admin.site.register(InstitutionType)
admin.site.register(ImageDefaultPlaceHolder)