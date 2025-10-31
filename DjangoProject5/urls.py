from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
def home(request):
    return render(request, 'home.html')

def discover(request):
    return render(request, 'discover.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('discover/', discover, name='discover'),
    path('usuarios/', include("usuarios.urls")),
    path('productos/', include('productos.urls')),

path('ia/', include('ia.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
