#!/usr/bin/env python
"""
Script para crear un usuario administrador del sistema.
Este usuario tendrá acceso completo para agregar y gestionar productos.
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject5.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

def crear_usuario_admin():
    print("🔧 Creando usuario administrador...")
    
    username = "admin"
    email = "admin@emprendeapp.com"
    password = "admin123"  # Puedes cambiar esta contraseña
    
    # Verificar si ya existe
    if User.objects.filter(username=username).exists():
        print(f"⚠️  El usuario '{username}' ya existe.")
        user = User.objects.get(username=username)
        
        # Verificar si tiene perfil
        if not hasattr(user, 'perfil'):
            PerfilUsuario.objects.create(user=user, rol='admin')
            print(f"✅ Se creó el perfil de administrador para '{username}'")
        else:
            # Actualizar a admin si no lo es
            if user.perfil.rol != 'admin':
                user.perfil.rol = 'admin'
                user.perfil.save()
                print(f"✅ Se actualizó '{username}' a rol de administrador")
            else:
                print(f"✅ El usuario '{username}' ya es administrador")
    else:
        # Crear nuevo usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        # Crear perfil de administrador
        PerfilUsuario.objects.create(user=user, rol='admin')
        
        print(f"✅ Usuario administrador creado exitosamente!")
    
    print("\n" + "="*50)
    print("📋 CREDENCIALES DE ACCESO:")
    print("="*50)
    print(f"Usuario: {username}")
    print(f"Contraseña: {password}")
    print(f"Email: {email}")
    print("="*50)
    print("\n✨ Ahora puedes iniciar sesión y agregar productos!\n")

if __name__ == "__main__":
    crear_usuario_admin()
