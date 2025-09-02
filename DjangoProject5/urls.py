from django.contrib import admin
from django.urls import path
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def discover(request):
    return render(request, 'discover.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),                 # Ruta principal
    path('discover/', discover, name='discover') # Nueva ruta
]
