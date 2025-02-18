# utils.py
import random
from django.utils import timezone

def generate_otp():
    """Génère un OTP à 6 chiffres."""
    return str(random.randint(100000, 999999))

def send_otp_console(phone_number, otp):
    """Affiche l’OTP dans la console (simule l'envoi par SMS)."""
    print(f"🔐 OTP pour {phone_number} : {otp} (Valide 10 minutes)")

