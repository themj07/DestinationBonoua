from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from blog.models import Article
from django.db.models import Count

from .models import DefaultPlaceHolderPersonne, Institution, InstitutionType, Toursisme, ToursismeType, CommentaireTourisme

# Create your views here.

def index(request):
    institutions = Institution.objects.all()  # Récupère toutes les institutions
    types_tourisme = ToursismeType.objects.all()
    types_institut = InstitutionType.objects.all()
    all_blogs = Article.objects.all().annotate(comment_count=Count("comments"))

    datas = {
        'institutions': institutions,
        'types_tourisme' : types_tourisme,
        'types_institut' : types_institut,
        'all_blogs': all_blogs,

    }
    return render(request, 'index.html', datas)


def error_404(request):
    datas = {}
    return render(request, '404.html', datas)


def places_tourismes(request):
    types_tourisme = ToursismeType.objects.all()
    all_blogs = Article.objects.all().annotate(comment_count=Count("comments"))

    datas = {
        'types_tourisme' : types_tourisme,
        'all_blogs': all_blogs,

    }
    return render(request, 'placesTourismes.html', datas)



def hotel(request, type_id):
    type_selected = get_object_or_404(ToursismeType, id=type_id)
    tourismes = Toursisme.objects.filter(type=type_selected)
    datas = {
        'tourismes': tourismes,
        'type_selected': type_selected
    }
    return render(request, 'hotels.html', datas)




def hotel_single(request, tourisme_id):
    all_blogs = Article.objects.all().annotate(comment_count=Count("comments"))
    tourisme = get_object_or_404(Toursisme, id=tourisme_id)
    commentaires = CommentaireTourisme.objects.filter(tourisme=tourisme)
    other_institutions = Institution.objects.exclude(id=tourisme_id)[:5]
    image_default = DefaultPlaceHolderPersonne.objects.all()

    if request.method == "POST":
        note = request.POST.get('stars')  # Récupération de la note
        commentaire = request.POST.get('commentaire')

        if note and commentaire:
            CommentaireTourisme.objects.create(
                tourisme=tourisme,
                user=request.user,  # ✅ Utilisateur connecté
                note=int(note),
                commentaire=commentaire
            )
            messages.success(request, "Votre commentaire a été ajouté.")
            return redirect('hotel-single', tourisme_id=tourisme.id)  # Rafraîchir la page

    datas = {
        'tourisme': tourisme,
        'commentaires': commentaires,
        'other_institutions': other_institutions,
        'image_default': image_default,
        'all_blogs': all_blogs,

    }
    return render(request, 'hotel-single.html', datas)


# 🔹 Page listant tous les types d’institutions (ex: Hôpital, Mairie, etc.)
def places_instituts(request):
    types_institut = InstitutionType.objects.all()
    all_blogs = Article.objects.all().annotate(comment_count=Count("comments"))
    datas = {
        'types_institut': types_institut,
        'all_blogs': all_blogs,

    }
    return render(request, 'placesInstituts.html', datas)


# 🔹 Page listant toutes les institutions d'un type donné
def instituts(request, type_id):
    type_selected = get_object_or_404(InstitutionType, id=type_id)
    institutions = Institution.objects.filter(type=type_selected)
    datas = {
        'institutions': institutions,
        'type_selected': type_selected
    }
    return render(request, 'instituts.html', datas)


# 🔹 Page affichant le détail d’une institution spécifique
def places_single_institut(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    default_placeholder = DefaultPlaceHolderPersonne.objects.filter(name="default").first()
    other_institutions = Institution.objects.exclude(id=institution_id)[:5]  # Afficher d'autres institutions pour la sidebar
    datas = {
        'institution': institution,
        'other_institutions': other_institutions,
        'default_placeholder': default_placeholder,
    }
    return render(request, 'places-single-institut.html', datas)




def places_single_tourisme(request):
    datas = {}
    return render(request, 'places-single-tourisme.html', datas)




