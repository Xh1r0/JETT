from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from .models import CustomUser, EmailVerification
import uuid

# ======================
# 🏠 Landing Page
# ======================
def index(request):
    return render(request, 'index.html')


# ======================
# 🧾 Register User (AJAX)
# ======================
def register_user(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Cek apakah email sudah dipakai
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email sudah digunakan.'})

        # Buat user baru
        user = CustomUser.objects.create_user(full_name=full_name, email=email, password=password)
        user.is_active = False  # belum aktif sebelum verifikasi
        user.save()

        # Buat token verifikasi email
        token = str(uuid.uuid4())
        EmailVerification.objects.create(user=user, token=token)

        # Kirim email verifikasi
        verification_link = request.build_absolute_uri(reverse('verify_email', args=[token]))
        send_mail(
            subject='Verifikasi Email Akun JETT',
            message=f'Halo {full_name},\n\nKlik link berikut untuk verifikasi akun kamu:\n{verification_link}\n\nTerima kasih telah mendaftar di JETT!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({'status': 'success', 'message': 'Akun berhasil dibuat! Silakan cek email untuk verifikasi.'})

    return JsonResponse({'status': 'error', 'message': 'Metode tidak valid.'})


# ======================
# 🔑 Login User (AJAX)
# ======================
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Login berhasil!'})
            else:
                return JsonResponse({'status': 'warning', 'message': 'Akun belum diverifikasi.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Email atau password salah.'})

    return JsonResponse({'status': 'error', 'message': 'Metode tidak valid.'})


# ======================
# 🚪 Logout User
# ======================
def logout_user(request):
    logout(request)
    messages.success(request, "Berhasil logout.")
    return redirect('index')


# ======================
# ✉️ Verifikasi Email
# ======================
def verify_email(request, token):
    try:
        verification = get_object_or_404(EmailVerification, token=token)
        user = verification.user
        user.is_active = True
        user.save()

        verification.delete()  # token dihapus setelah digunakan

        messages.success(request, "Email berhasil diverifikasi! Silakan login.")
        return redirect('index')

    except Exception as e:
        messages.error(request, "Token verifikasi tidak valid atau sudah kadaluarsa.")
        return redirect('index')
