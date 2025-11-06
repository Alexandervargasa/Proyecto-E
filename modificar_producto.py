#!/usr/bin/env python
"""
Script para modificar productos desde la terminal.
Uso: python modificar_producto.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject5.settings')
django.setup()

from productos.models import Producto

def listar_productos():
    """Muestra todos los productos"""
    productos = Producto.objects.all()
    print("\n📦 PRODUCTOS DISPONIBLES:")
    print("=" * 80)
    for p in productos:
        print(f"ID: {p.id} | {p.nombre} | ${p.precio} | Stock: {p.stock}")
    print("=" * 80)

def modificar_producto():
    """Modifica un producto por su ID"""
    listar_productos()
    
    producto_id = input("\n🔍 Ingresa el ID del producto a modificar: ")
    
    try:
        producto = Producto.objects.get(id=producto_id)
        print(f"\n✅ Producto encontrado: {producto.nombre}")
        print("\n¿Qué deseas modificar?")
        print("1. Nombre")
        print("2. Descripción")
        print("3. Precio")
        print("4. Stock")
        print("5. Marca")
        print("6. Categoría")
        print("7. Número de vendedor")
        print("8. Todo")
        
        opcion = input("\nSelecciona una opción (1-8): ")
        
        if opcion == "1":
            nuevo_nombre = input(f"Nombre actual: {producto.nombre}\nNuevo nombre: ")
            producto.nombre = nuevo_nombre
        elif opcion == "2":
            nueva_desc = input(f"Descripción actual: {producto.descripcion}\nNueva descripción: ")
            producto.descripcion = nueva_desc
        elif opcion == "3":
            nuevo_precio = input(f"Precio actual: ${producto.precio}\nNuevo precio: ")
            producto.precio = nuevo_precio
        elif opcion == "4":
            nuevo_stock = input(f"Stock actual: {producto.stock}\nNuevo stock: ")
            producto.stock = nuevo_stock
        elif opcion == "5":
            nueva_marca = input(f"Marca actual: {producto.marca}\nNueva marca: ")
            producto.marca = nueva_marca
        elif opcion == "6":
            nueva_categoria = input(f"Categoría actual: {producto.categoria}\nNueva categoría: ")
            producto.categoria = nueva_categoria
        elif opcion == "7":
            nuevo_numero = input(f"Número actual: {producto.numero_vendedor}\nNuevo número: ")
            producto.numero_vendedor = nuevo_numero
        elif opcion == "8":
            producto.nombre = input(f"Nombre [{producto.nombre}]: ") or producto.nombre
            producto.descripcion = input(f"Descripción [{producto.descripcion}]: ") or producto.descripcion
            producto.precio = input(f"Precio [{producto.precio}]: ") or producto.precio
            producto.stock = input(f"Stock [{producto.stock}]: ") or producto.stock
            producto.marca = input(f"Marca [{producto.marca}]: ") or producto.marca
            producto.categoria = input(f"Categoría [{producto.categoria}]: ") or producto.categoria
            producto.numero_vendedor = input(f"Número vendedor [{producto.numero_vendedor}]: ") or producto.numero_vendedor
        
        producto.save()
        print(f"\n✅ Producto '{producto.nombre}' actualizado exitosamente!")
        
    except Producto.DoesNotExist:
        print(f"\n❌ No se encontró ningún producto con ID {producto_id}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🛠️  MODIFICADOR DE PRODUCTOS")
    print("="*80)
    modificar_producto()
