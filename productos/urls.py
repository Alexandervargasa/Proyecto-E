from django.urls import path
from . import views

urlpatterns = [
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
]
