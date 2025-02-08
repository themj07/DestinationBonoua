from django.shortcuts import render


def forgot(request):
    datas = {}
    return render(request, 'forgot.html', datas)


def login(request):
    datas = {}
    return render(request, 'login.html', datas)


def register(request):
    datas = {}
    return render(request, 'register.html', datas)
