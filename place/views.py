from django.shortcuts import render

# Create your views here.

def index(request):
    datas = {
    }
    return render(request, 'index.html', datas)


def error_404(request):
    datas = {}
    return render(request, '404.html', datas)


def hotel(request):
    datas = {}
    return render(request, 'hotel.html', datas)


def hotel_single(request):
    datas = {}
    return render(request, 'hotel-single.html', datas)


def places(request):
    datas = {}
    return render(request, 'places.html', datas)


def places_single(request):
    datas = {}
    return render(request, 'places-single.html', datas)


def service(request):
    datas = {}
    return render(request, 'service.html', datas)


def service_s2(request):
    datas = {}
    return render(request, 'service-s2.html', datas)


def service_single(request):
    datas = {}
    return render(request, 'service-single.html', datas)