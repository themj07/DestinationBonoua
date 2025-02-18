from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile
from .utils import generate_otp, send_otp_console
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


def forgot(request):
    datas = {}
    return render(request, 'forgot.html', datas)



@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")


def register(request):
    """Inscription et génération d’OTP"""
    if request.method == 'POST':
        username = request.POST.get('username')  # ✅ Ajoutez ceci
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if not username:
            messages.error(request, "Le nom d'utilisateur est requis.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà pris.")
            return redirect('register')

        if UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Numéro de téléphone déjà utilisé.")
            return redirect('register')

        # ✅ Correction : Utiliser `create_user` avec `username`
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        otp = generate_otp()
        otp_expiry = timezone.now() + timezone.timedelta(minutes=10)

        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            otp=otp,
            otp_expiry=otp_expiry
        )

        request.session['phone_number'] = phone_number

        # Affiche l’OTP dans la console
        send_otp_console(phone_number, otp)

        messages.success(request, "Un OTP a été généré (voir la console).")
        return redirect('verify_otp')

    return render(request, 'register.html')


def verify_otp(request):
    """Vérification de l’OTP (session)"""
    phone_number = request.session.get('phone_number')

    if not phone_number:
        messages.error(request, "Session expirée. Veuillez vous réinscrire.")
        return redirect('register')

    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            profile = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            messages.error(request, "Profil non trouvé.")
            return redirect('verify_otp')

        if profile.is_otp_expired():
            messages.error(request, "L'OTP a expiré. Veuillez réessayer.")
            return redirect('verify_otp')

        if profile.otp == otp:
            profile.is_phone_verified = True
            profile.otp = None
            profile.otp_expiry = None
            profile.save()

            messages.success(request, "Vérification réussie. Vous pouvez vous connecter.")
            return redirect('login')
        else:
            messages.error(request, "OTP incorrect.")
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')


def get_user_by_identifier(identifier):
    """Recherche l'utilisateur par numéro ou username."""
    try:
        profile = UserProfile.objects.get(phone_number=identifier)
        return profile.user
    except UserProfile.DoesNotExist:
        try:
            return User.objects.get(username=identifier)
        except User.DoesNotExist:
            return None


def user_login(request):
    """Connexion avec numéro ou username + Envoi OTP."""
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # Numéro ou username
        password = request.POST.get('password')

        user = get_user_by_identifier(identifier)

        if user is None:
            messages.error(request, "Utilisateur introuvable.")
            return redirect('login')

        # Vérification du mot de passe
        authenticated_user = authenticate(request, username=user.username, password=password)
        if authenticated_user is not None:
            # Générer et sauvegarder l'OTP
            profile = UserProfile.objects.get(user=user)
            otp = generate_otp()
            profile.otp = otp
            profile.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
            profile.save()

            # Enregistrer dans la session pour vérification
            request.session['username'] = user.username

            # Envoyer l’OTP dans la console
            send_otp_console(profile.phone_number, otp)

            messages.success(request, "Un OTP a été envoyé. Vérifiez votre téléphone.")
            return redirect('verify_otp_login')
        else:
            messages.error(request, "Mot de passe incorrect.")
            return redirect('login')

    return render(request, 'login.html')



def verify_otp_login(request):
    """Vérification OTP et connexion."""
    username = request.session.get('username')

    if not username:
        messages.error(request, "Session expirée. Veuillez vous reconnecter.")
        return redirect('login')

    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            profile = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
            return redirect('login')

        if profile.is_otp_expired():
            messages.error(request, "L'OTP a expiré. Veuillez réessayer.")
            return redirect('login')

        if profile.otp == otp:
            profile.otp = None
            profile.otp_expiry = None
            profile.save()

            user = profile.user

            # ✅ Forcer l’authentification avec le backend par défaut
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            if request.user.is_authenticated:
                messages.success(request, "Connexion réussie.")
                return redirect('index')
            else:
                messages.error(request, "Erreur lors de la connexion.")
                return redirect('login')

        else:
            messages.error(request, "OTP incorrect. Veuillez réessayer.")

    return render(request, 'verify_otp_login.html')