from django.shortcuts import render

def about(request):
    datas = {}
    return render(request, 'about.html', datas)


def author(request):
    datas = {}
    return render(request, 'author.html', datas)


def blog(request):
    datas = {}
    return render(request, 'blog.html', datas)


def blog_left_sidebar(request):
    datas = {}
    return render(request, 'blog-left-sidebar.html', datas)


def blog_single(request):
    datas = {}
    return render(request, 'blog-single.html', datas)


def contact(request):
    datas = {}
    return render(request, 'contact.html', datas)


def faq(request):
    datas = {}
    return render(request, 'faq.html', datas)
