from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=10, choices=ROLES, default='cliente')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
    
    def es_admin(self):
        return self.rol == 'admin'
