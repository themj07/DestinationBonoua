from django.contrib import admin
from .models import Institution, InstitutionType, DefaultPlaceHolderPersonne, Toursisme, ToursismeType, CommentaireTourisme


# Register your models here.

admin.site.register(Institution)
admin.site.register(InstitutionType)
admin.site.register(DefaultPlaceHolderPersonne)
admin.site.register(ToursismeType)
admin.site.register(Toursisme)
admin.site.register(CommentaireTourisme)

