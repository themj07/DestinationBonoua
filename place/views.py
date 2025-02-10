from django.shortcuts import get_object_or_404, render

from .models import ImageDefaultPlaceHolder, Institution, InstitutionType

# Create your views here.

def index(request):
    institutions = Institution.objects.all()  # Récupère toutes les institutions
    datas = {
        'institutions': institutions,
    }
    return render(request, 'index.html', datas)


def error_404(request):
    datas = {}
    return render(request, '404.html', datas)


def hotel(request):
    datas = {}
    return render(request, 'hotels.html', datas)


def hotel_single(request):
    datas = {}
    return render(request, 'hotel-single.html', datas)


# 🔹 Page listant tous les types d’institutions (ex: Hôpital, Mairie, etc.)
def places_instituts(request):
    types = InstitutionType.objects.all()
    datas = {
        'types': types
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
    default_placeholder = ImageDefaultPlaceHolder.objects.filter(name="default").first()
    other_institutions = Institution.objects.exclude(id=institution_id)[:5]  # Afficher d'autres institutions pour la sidebar
    datas = {
        'institution': institution,
        'other_institutions': other_institutions,
        'default_placeholder': default_placeholder,
    }
    return render(request, 'places-single-institut.html', datas)


def places_tourismes(request):
    datas = {}
    return render(request, 'placesTourismes.html', datas)


def places_single_tourisme(request):
    datas = {}
    return render(request, 'places-single-tourisme.html', datas)


def service(request):
    datas = {}
    return render(request, 'service.html', datas)


def service_s2(request):
    datas = {}
    return render(request, 'service-s2.html', datas)


def service_single(request):
    datas = {}
    return render(request, 'service-single.html', datas)