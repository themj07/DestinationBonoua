from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Contact
from django.contrib import messages
from blog import models
from django.db.models import Count



def about(request):
    datas = {}
    return render(request, 'about.html', datas)



def author(request):
    datas = {}
    return render(request, 'author.html', datas)



def blogs(request):
    all_blogs = Article.objects.all().annotate(comment_count=Count("comments"))
    datas = {
        'all_blogs': all_blogs
    }
    return render(request, 'blogs.html', datas)



def blog_single(request, blog_id):
    """Affiche un article et permet d'ajouter un commentaire avec un message de confirmation."""
    selected_blog = get_object_or_404(Article, id=blog_id)
    commentaires = Comment.objects.filter(blog=selected_blog).order_by('-created_at')

    if request.method == "POST":
        if request.user.is_authenticated:  # Vérifie que l'utilisateur est connecté
            content = request.POST.get('content')  # Récupération du commentaire

            if content.strip():  # Vérifie si le commentaire n'est pas vide
                Comment.objects.create(
                    blog=selected_blog,
                    user=request.user,
                    content=content
                )
                messages.success(request, "✅ Votre commentaire a été ajouté avec succès !")
            else:
                messages.error(request, "⚠️ Votre commentaire ne peut pas être vide.")

        else:
            messages.error(request, "⚠️ Vous devez être connecté pour laisser un commentaire.")

        return redirect('blog-single', blog_id=selected_blog.id)  # Rafraîchir la page

    datas = {
        'selected_blog': selected_blog,
        'commentaires': commentaires,
    }
    return render(request, 'blog-single.html', datas)



def contact(request):
    if request.method == "POST":
        name = request.POST.get("name") if not request.user.is_authenticated else request.user.username
        email = request.POST.get("email") if not request.user.is_authenticated else request.user.email
        subject = request.POST.get("subject")
        message = request.POST.get("note")

        if name and email and subject and message:
            Contact.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, "✅ Votre message a été envoyé avec succès !")
        else:
            messages.error(request, "⚠️ Tous les champs sont obligatoires !")

        return redirect("contact")

    return render(request, "contact.html")



def faq(request):
    datas = {}
    return render(request, 'faq.html', datas)
