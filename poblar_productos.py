import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject5.settings')
django.setup()

from django.contrib.auth.models import User
from productos.models import Producto
from usuarios.models import PerfilUsuario

# Crear un usuario vendedor si no existe
vendedor, created = User.objects.get_or_create(
    username='vendedor_demo',
    defaults={
        'email': 'vendedor@ejemplo.com',
        'first_name': 'Juan',
        'last_name': 'Pérez'
    }
)

if created:
    vendedor.set_password('demo123')
    vendedor.save()
    # Crear perfil de usuario
    PerfilUsuario.objects.get_or_create(user=vendedor, defaults={'rol': 'cliente'})
    print(f"✅ Usuario vendedor creado: {vendedor.username}")
else:
    print(f"ℹ️ Usuario vendedor ya existe: {vendedor.username}")

# Lista de productos a crear
productos_data = [
    {
        'nombre': 'Gomitas Bon Bon Bum',
        'descripcion': 'Deliciosas gomitas con sabor a frutas tropicales. Perfectas para compartir en cualquier ocasión. Producto artesanal hecho con ingredientes naturales.',
        'precio': 5000,
        'stock': 50,
        'categoria': 'Dulces',
        'marca': 'Bon Bon Bum',
        'numero_vendedor': '3135436786',
        'clics_carrito': 25
    },
    {
        'nombre': 'Chocolate Artesanal',
        'descripcion': 'Chocolate premium 70% cacao, elaborado artesanalmente con cacao colombiano de la mejor calidad. Sin azúcares añadidos.',
        'precio': 8500,
        'stock': 30,
        'categoria': 'Dulces',
        'marca': 'ChocoArt',
        'numero_vendedor': '3201234567',
        'clics_carrito': 42
    },
    {
        'nombre': 'Café Colombiano Premium',
        'descripcion': 'Café 100% colombiano de origen, tostado artesanalmente. Notas de caramelo y chocolate. Bolsa de 500g.',
        'precio': 25000,
        'stock': 45,
        'categoria': 'Bebidas',
        'marca': 'Café del Valle',
        'numero_vendedor': '3151234567',
        'clics_carrito': 38
    },
    {
        'nombre': 'Miel de Abejas Orgánica',
        'descripcion': 'Miel 100% natural y orgánica, producida en los campos colombianos. Frasco de 500ml. Rica en antioxidantes.',
        'precio': 18000,
        'stock': 25,
        'categoria': 'Alimentos',
        'marca': 'Mieles del Campo',
        'numero_vendedor': '3187654321',
        'clics_carrito': 15
    },
    {
        'nombre': 'Galletas de Avena Caseras',
        'descripcion': 'Galletas artesanales con avena, pasas y nueces. Sin preservantes. Paquete de 12 unidades.',
        'precio': 7000,
        'stock': 60,
        'categoria': 'Panadería',
        'marca': 'Delicias Caseras',
        'numero_vendedor': '3165432109',
        'clics_carrito': 28
    },
    {
        'nombre': 'Mermelada de Mora Natural',
        'descripcion': 'Mermelada artesanal de mora sin colorantes ni preservantes artificiales. Frasco de 300g.',
        'precio': 9500,
        'stock': 35,
        'categoria': 'Alimentos',
        'marca': 'Frutas del Bosque',
        'numero_vendedor': '3145678901',
        'clics_carrito': 19
    },
    {
        'nombre': 'Arepa de Chócolo Congelada',
        'descripcion': 'Arepas de chócolo colombianas hechas a mano, listas para calentar. Paquete de 6 unidades.',
        'precio': 12000,
        'stock': 40,
        'categoria': 'Alimentos',
        'marca': 'Arepas Tradicionales',
        'numero_vendedor': '3132345678',
        'clics_carrito': 22
    },
    {
        'nombre': 'Salsa Picante Artesanal',
        'descripcion': 'Salsa picante elaborada con chiles frescos y especias naturales. Nivel medio-alto. Frasco de 250ml.',
        'precio': 8000,
        'stock': 50,
        'categoria': 'Condimentos',
        'marca': 'Picante Casero',
        'numero_vendedor': '3178901234',
        'clics_carrito': 31
    },
    {
        'nombre': 'Pan Integral Artesanal',
        'descripcion': 'Pan integral hecho con masa madre natural, sin aditivos. Ideal para una dieta saludable. Unidad de 500g.',
        'precio': 6500,
        'stock': 20,
        'categoria': 'Panadería',
        'marca': 'Pan del Campo',
        'numero_vendedor': '3198765432',
        'clics_carrito': 17
    },
    {
        'nombre': 'Queso Campesino',
        'descripcion': 'Queso fresco artesanal elaborado con leche de vaca de alta calidad. Sabor suave y cremoso. 500g.',
        'precio': 15000,
        'stock': 30,
        'categoria': 'Lácteos',
        'marca': 'Quesería la Vaca',
        'numero_vendedor': '3123456789',
        'clics_carrito': 35
    },
    {
        'nombre': 'Jugo Natural de Lulo',
        'descripcion': 'Jugo 100% natural de lulo sin azúcar añadida. Botella de 1 litro. Refrigerado.',
        'precio': 10000,
        'stock': 45,
        'categoria': 'Bebidas',
        'marca': 'Jugos Naturales',
        'numero_vendedor': '3156789012',
        'clics_carrito': 29
    },
    {
        'nombre': 'Empanadas Congeladas',
        'descripcion': 'Empanadas colombianas de carne, listas para freír. Paquete de 10 unidades. Receta tradicional.',
        'precio': 15000,
        'stock': 55,
        'categoria': 'Alimentos',
        'marca': 'Empanadas Criollas',
        'numero_vendedor': '3167890123',
        'clics_carrito': 40
    },
    {
        'nombre': 'Arequipe Artesanal',
        'descripcion': 'Arequipe tradicional colombiano hecho con leche fresca. Textura cremosa perfecta. Frasco de 400g.',
        'precio': 11000,
        'stock': 38,
        'categoria': 'Dulces',
        'marca': 'Dulces de Leche',
        'numero_vendedor': '3189012345',
        'clics_carrito': 26
    },
    {
        'nombre': 'Té de Hierbas Aromáticas',
        'descripcion': 'Mezcla especial de hierbas colombianas: manzanilla, yerbabuena y toronjil. Caja de 20 sobres.',
        'precio': 7500,
        'stock': 42,
        'categoria': 'Bebidas',
        'marca': 'Hierbas del Campo',
        'numero_vendedor': '3190123456',
        'clics_carrito': 18
    },
    {
        'nombre': 'Bocadillo de Guayaba',
        'descripcion': 'Bocadillo tradicional veleño elaborado con guayaba 100% natural. Barra de 300g.',
        'precio': 6000,
        'stock': 70,
        'categoria': 'Dulces',
        'marca': 'Dulces Veleños',
        'numero_vendedor': '3112345678',
        'clics_carrito': 33
    },
    {
        'nombre': 'Salchichón Artesanal',
        'descripcion': 'Salchichón ahumado artesanalmente con especias naturales. Sin conservantes. 400g.',
        'precio': 16000,
        'stock': 28,
        'categoria': 'Carnes',
        'marca': 'Carnes Selectas',
        'numero_vendedor': '3134567890',
        'clics_carrito': 21
    },
    {
        'nombre': 'Brownies de Chocolate',
        'descripcion': 'Brownies caseros con chocolate belga. Súper húmedos y deliciosos. Paquete de 6 unidades.',
        'precio': 14000,
        'stock': 32,
        'categoria': 'Panadería',
        'marca': 'Postres Gourmet',
        'numero_vendedor': '3145678902',
        'clics_carrito': 36
    },
    {
        'nombre': 'Granola Artesanal',
        'descripcion': 'Granola hecha con avena, miel, frutos secos y semillas. Ideal para el desayuno. Bolsa de 500g.',
        'precio': 13000,
        'stock': 40,
        'categoria': 'Cereales',
        'marca': 'Granos Saludables',
        'numero_vendedor': '3167890124',
        'clics_carrito': 24
    },
    {
        'nombre': 'Aceite de Oliva Extra Virgen',
        'descripcion': 'Aceite de oliva importado, prensado en frío. Ideal para ensaladas y cocina mediterránea. 500ml.',
        'precio': 32000,
        'stock': 22,
        'categoria': 'Aceites',
        'marca': 'Olivos del Mediterráneo',
        'numero_vendedor': '3178901235',
        'clics_carrito': 14
    },
    {
        'nombre': 'Papas Criollas Fritas',
        'descripcion': 'Papas criollas precocidas y congeladas, listas para freír. Bolsa de 1kg. Producto colombiano.',
        'precio': 9000,
        'stock': 48,
        'categoria': 'Alimentos',
        'marca': 'Papas del Campo',
        'numero_vendedor': '3189012346',
        'clics_carrito': 27
    }
]

# Crear productos
productos_creados = 0
productos_existentes = 0

for producto_data in productos_data:
    producto, created = Producto.objects.get_or_create(
        nombre=producto_data['nombre'],
        defaults={
            'descripcion': producto_data['descripcion'],
            'precio': producto_data['precio'],
            'stock': producto_data['stock'],
            'categoria': producto_data['categoria'],
            'marca': producto_data['marca'],
            'numero_vendedor': producto_data['numero_vendedor'],
            'clics_carrito': producto_data['clics_carrito'],
            'usuario': vendedor
        }
    )
    
    if created:
        productos_creados += 1
        print(f"✅ Producto creado: {producto.nombre}")
    else:
        productos_existentes += 1
        print(f"ℹ️ Producto ya existe: {producto.nombre}")

print("\n" + "="*50)
print(f"📊 RESUMEN:")
print(f"   ✅ Productos nuevos creados: {productos_creados}")
print(f"   ℹ️ Productos que ya existían: {productos_existentes}")
print(f"   📦 Total de productos en la BD: {Producto.objects.count()}")
print("="*50)
print("\n🎉 ¡Base de datos poblada exitosamente!")
