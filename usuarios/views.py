from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import RegistroForm


# 👉 Registro de usuarios
def register(request):
    if request.user.is_authenticated:
        return redirect("home")  # Si ya está logueado, no debería registrarse otra vez

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu cuenta ha sido creada con éxito! ✅")
            return redirect("login")  # Después de registrarse va al login
    else:
        form = RegistroForm()
    return render(request, "usuarios/register.html", {"form": form})


# 👉 Login de usuarios
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")  # Si ya está logueado, no mostrar login otra vez

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido {username}! 🚀")
                return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos ❌")
    else:
        form = AuthenticationForm()

    return render(request, "usuarios/login.html", {"form": form})


# 👉 Logout de usuarios
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión 👋")
    return redirect("login")
