from blog.models import *
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.db.models.query_utils import Q
from .forms import UserRegistrationForm , SetPasswordForm, PasswordResetForm, UserLoginForm
from .tokens import account_activation_token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from .models import NewsletterSubscriber

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('index')


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="register.html",
        context={"form": form}
        )


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset Request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                
                email = EmailMessage(subject, message, to=[associated_user.email])
                email.content_subtype = "html"  # ⬅️ Ajoute cette ligne pour envoyer en HTML
                
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('index')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="reset_password.html", 
        context={"form": form}
    )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'reset_password_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("index")


def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user) 
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("index")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="login.html",
        context={"form": form}
        )


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    if email.send():
        messages.success(request, f'Cher {user}, consultez votre adresse {to_email} et cliquez sur \
                le lien pour completer votre inscription. Note: il pourrait etre dans le dossier spam.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Récupère l'email du formulaire

        # Vérifier si l'email est déjà enregistré
        if NewsletterSubscriber.objects.filter(email=email).exists():
            messages.warning(request, 'Cet email est déjà enregistré !')
        else:
            # Enregistrer l'email dans la base de données
            NewsletterSubscriber.objects.create(email=email)

            # Récupérer le protocole et le domaine
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            domain = current_site.domain

            # Contexte pour le template HTML
            context = {
                'email': email,
                'protocol': protocol,
                'domain': domain,
            }

            # Charger et rendre le template HTML
            html_message = render_to_string('newsletter_confirmation.html', context)

            # Envoyer un email de confirmation
            subject = 'Confirmation d\'inscription à la newsletter'
            message = 'Merci de vous être inscrit à notre newsletter !'  # Version texte brut
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    html_message=html_message  # Utiliser le template HTML comme corps de l'email
                )
                messages.success(request, 'Vous êtes maintenant inscrit à notre newsletter !')
            except Exception as e:
                messages.error(request, f'Une erreur s\'est produite : {e}')

        # Rediriger l'utilisateur vers la page précédente ou une page de confirmation
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # Si la méthode n'est pas POST, rediriger vers la page d'accueil
    return HttpResponseRedirect('/')


def unsubscribe_newsletter(request, email):
    # Récupérer l'abonné ou renvoyer une erreur 404 si non trouvé
    subscriber = get_object_or_404(NewsletterSubscriber, email=email)

    # Supprimer l'abonné de la base de données
    subscriber.delete()

    # Afficher un message de confirmation
    messages.success(request, 'Vous avez été désabonné de notre newsletter.')

    # Rediriger vers la page d'accueil ou une page de confirmation
    return HttpResponseRedirect('/')