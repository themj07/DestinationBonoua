from django.contrib import admin
from .models import Article, Contact , Comment

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Contact)