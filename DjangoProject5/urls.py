from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.urls import path, include
def home(request):
    return render(request, 'home.html')

def discover(request):
    return render(request, 'discover.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('discover/', discover, name='discover'),
    path('usuarios/', include("usuarios.urls")),  # 👈 ahora van bajo /usuarios/

path('ia/', include('ia.urls')),
]

