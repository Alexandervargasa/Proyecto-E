from django.urls import path
from . import views

urlpatterns = [
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
]
