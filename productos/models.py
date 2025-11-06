from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    clics_carrito = models.PositiveIntegerField(default=0)  # Contador de clics
    numero_vendedor = models.CharField(max_length=20, blank=True, null=True)  # Número del vendedor
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)  # Propietario del producto

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['-clics_carrito', '-fecha_registro']

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/Pimages')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"