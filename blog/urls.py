from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('author/', views.author, name='author'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog-single/', views.blog_single, name='blog-single'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
]
