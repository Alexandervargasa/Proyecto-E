from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm

def register(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu cuenta ha sido creada con éxito!")
            return redirect("home")  # o a donde quieras redirigir
    else:
        form = RegistroForm()
    return render(request, "usuarios/register.html", {"form": form})
