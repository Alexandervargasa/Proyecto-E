import os
import django
import requests
from io import BytesIO
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject5.settings')
django.setup()

from django.contrib.auth.models import User
from productos.models import Producto, ImagenProducto
from usuarios.models import PerfilUsuario

# Obtener el usuario vendedor
try:
    vendedor = User.objects.get(username='vendedor_demo')
except User.DoesNotExist:
    vendedor = User.objects.create_user(
        username='vendedor_demo',
        email='vendedor@ejemplo.com',
        password='demo123',
        first_name='Juan',
        last_name='Pérez'
    )
    PerfilUsuario.objects.get_or_create(user=vendedor, defaults={'rol': 'cliente'})

# URLs de imágenes genéricas de productos (usando placeholder)
def get_product_image_url(seed):
    """Genera URL de imagen placeholder con seed único"""
    return f"https://picsum.photos/seed/{seed}/400/400"

# Lista completa de 79 productos adicionales
productos_adicionales = [
    # Bebidas (10)
    {'nombre': 'Limonada Natural', 'descripcion': 'Limonada casera con limón fresco y menta. Botella de 1L.', 'precio': 8000, 'stock': 40, 'categoria': 'Bebidas', 'marca': 'Refrescos Naturales', 'numero_vendedor': '3201234568', 'clics_carrito': 20},
    {'nombre': 'Cerveza Artesanal IPA', 'descripcion': 'Cerveza artesanal estilo IPA con lúpulos importados. 330ml.', 'precio': 12000, 'stock': 60, 'categoria': 'Bebidas', 'marca': 'Cervecería Local', 'numero_vendedor': '3202345679', 'clics_carrito': 45},
    {'nombre': 'Vino Tinto Reserva', 'descripcion': 'Vino tinto reserva de uva cabernet. Botella de 750ml.', 'precio': 45000, 'stock': 25, 'categoria': 'Bebidas', 'marca': 'Viñedos del Valle', 'numero_vendedor': '3203456780', 'clics_carrito': 18},
    {'nombre': 'Agua de Coco Natural', 'descripcion': 'Agua de coco 100% natural. Botella de 500ml.', 'precio': 6000, 'stock': 50, 'categoria': 'Bebidas', 'marca': 'Coco Fresh', 'numero_vendedor': '3204567891', 'clics_carrito': 22},
    {'nombre': 'Kombucha Jengibre', 'descripcion': 'Bebida probiótica fermentada con jengibre. Botella 400ml.', 'precio': 14000, 'stock': 30, 'categoria': 'Bebidas', 'marca': 'Kombucha Co', 'numero_vendedor': '3205678902', 'clics_carrito': 16},
    {'nombre': 'Smoothie de Frutos Rojos', 'descripcion': 'Smoothie natural con fresas, moras y arándanos. 500ml.', 'precio': 11000, 'stock': 35, 'categoria': 'Bebidas', 'marca': 'Smoothie Bar', 'numero_vendedor': '3206789013', 'clics_carrito': 25},
    {'nombre': 'Té Verde Matcha', 'descripcion': 'Té verde matcha premium importado de Japón. Lata 100g.', 'precio': 28000, 'stock': 20, 'categoria': 'Bebidas', 'marca': 'Matcha Premium', 'numero_vendedor': '3207890124', 'clics_carrito': 12},
    {'nombre': 'Leche de Almendras', 'descripcion': 'Bebida vegetal de almendras sin azúcar. Cartón de 1L.', 'precio': 13000, 'stock': 45, 'categoria': 'Bebidas', 'marca': 'Veggie Drinks', 'numero_vendedor': '3208901235', 'clics_carrito': 28},
    {'nombre': 'Horchata Casera', 'descripcion': 'Horchata tradicional de arroz y canela. Botella 1L.', 'precio': 9000, 'stock': 38, 'categoria': 'Bebidas', 'marca': 'Bebidas Tradicionales', 'numero_vendedor': '3209012346', 'clics_carrito': 19},
    {'nombre': 'Café Frío Latte', 'descripcion': 'Café frío tipo latte con leche. Listo para tomar. 350ml.', 'precio': 10000, 'stock': 42, 'categoria': 'Bebidas', 'marca': 'Coffee Cold', 'numero_vendedor': '3210123457', 'clics_carrito': 31},
    
    # Panadería y Repostería (15)
    {'nombre': 'Croissant de Mantequilla', 'descripcion': 'Croissant francés hojaldrado con mantequilla. Unidad.', 'precio': 4500, 'stock': 30, 'categoria': 'Panadería', 'marca': 'Panadería Francesa', 'numero_vendedor': '3211234568', 'clics_carrito': 35},
    {'nombre': 'Muffins de Arándanos', 'descripcion': 'Muffins caseros con arándanos frescos. Paquete de 4.', 'precio': 12000, 'stock': 25, 'categoria': 'Panadería', 'marca': 'Sweet Bakery', 'numero_vendedor': '3212345679', 'clics_carrito': 27},
    {'nombre': 'Donas Glaseadas', 'descripcion': 'Donas esponjosas con glaseado de colores. Caja de 6.', 'precio': 15000, 'stock': 35, 'categoria': 'Panadería', 'marca': 'Donas Felices', 'numero_vendedor': '3213456780', 'clics_carrito': 42},
    {'nombre': 'Pan de Bono', 'descripcion': 'Pan de bono colombiano tradicional. Bolsa de 10 unidades.', 'precio': 8000, 'stock': 50, 'categoria': 'Panadería', 'marca': 'Pan Colombiano', 'numero_vendedor': '3214567891', 'clics_carrito': 38},
    {'nombre': 'Cheesecake de Fresa', 'descripcion': 'Cheesecake cremoso con cobertura de fresas. Porción.', 'precio': 18000, 'stock': 20, 'categoria': 'Panadería', 'marca': 'Postres Finos', 'numero_vendedor': '3215678902', 'clics_carrito': 24},
    {'nombre': 'Cupcakes Vainilla', 'descripcion': 'Cupcakes de vainilla con buttercream. Caja de 4.', 'precio': 16000, 'stock': 28, 'categoria': 'Panadería', 'marca': 'Cupcake House', 'numero_vendedor': '3216789013', 'clics_carrito': 29},
    {'nombre': 'Tarta de Manzana', 'descripcion': 'Tarta casera de manzana con canela. Porción individual.', 'precio': 13000, 'stock': 22, 'categoria': 'Panadería', 'marca': 'Tartas Artesanales', 'numero_vendedor': '3217890124', 'clics_carrito': 21},
    {'nombre': 'Bagels Integrales', 'descripcion': 'Bagels integrales recién horneados. Bolsa de 6.', 'precio': 10000, 'stock': 32, 'categoria': 'Panadería', 'marca': 'Bagel Shop', 'numero_vendedor': '3218901235', 'clics_carrito': 17},
    {'nombre': 'Alfajores de Dulce de Leche', 'descripcion': 'Alfajores rellenos de dulce de leche. Caja de 6.', 'precio': 14000, 'stock': 40, 'categoria': 'Panadería', 'marca': 'Dulces del Sur', 'numero_vendedor': '3219012346', 'clics_carrito': 33},
    {'nombre': 'Galletas de Chocolate Chip', 'descripcion': 'Galletas con chips de chocolate. Paquete de 12.', 'precio': 9000, 'stock': 45, 'categoria': 'Panadería', 'marca': 'Cookie Factory', 'numero_vendedor': '3220123457', 'clics_carrito': 36},
    {'nombre': 'Pan Brioche', 'descripcion': 'Pan brioche francés suave y esponjoso. Unidad 400g.', 'precio': 11000, 'stock': 30, 'categoria': 'Panadería', 'marca': 'Pain Français', 'numero_vendedor': '3221234568', 'clics_carrito': 23},
    {'nombre': 'Torta de Zanahoria', 'descripcion': 'Torta de zanahoria con frosting de queso crema. Porción.', 'precio': 15000, 'stock': 18, 'categoria': 'Panadería', 'marca': 'Cake Corner', 'numero_vendedor': '3222345679', 'clics_carrito': 26},
    {'nombre': 'Panqueques Congelados', 'descripcion': 'Panqueques listos para calentar. Paquete de 10.', 'precio': 12000, 'stock': 38, 'categoria': 'Panadería', 'marca': 'Breakfast Quick', 'numero_vendedor': '3223456780', 'clics_carrito': 20},
    {'nombre': 'Scones de Arándano', 'descripcion': 'Scones ingleses con arándanos. Bolsa de 4.', 'precio': 13000, 'stock': 26, 'categoria': 'Panadería', 'marca': 'British Bakery', 'numero_vendedor': '3224567891', 'clics_carrito': 15},
    {'nombre': 'Churros Congelados', 'descripcion': 'Churros listos para freír. Bolsa de 15 unidades.', 'precio': 10000, 'stock': 42, 'categoria': 'Panadería', 'marca': 'Churros Express', 'numero_vendedor': '3225678902', 'clics_carrito': 30},
    
    # Lácteos y Derivados (10)
    {'nombre': 'Yogurt Griego Natural', 'descripcion': 'Yogurt griego sin azúcar. Envase de 500g.', 'precio': 9500, 'stock': 50, 'categoria': 'Lácteos', 'marca': 'Greek Yogurt Co', 'numero_vendedor': '3226789013', 'clics_carrito': 34},
    {'nombre': 'Mantequilla Artesanal', 'descripcion': 'Mantequilla hecha con crema fresca. Barra de 250g.', 'precio': 12000, 'stock': 35, 'categoria': 'Lácteos', 'marca': 'Mantequilla Premium', 'numero_vendedor': '3227890124', 'clics_carrito': 22},
    {'nombre': 'Queso Mozzarella', 'descripcion': 'Queso mozzarella fresco ideal para pizza. 400g.', 'precio': 14000, 'stock': 40, 'categoria': 'Lácteos', 'marca': 'Quesos Italianos', 'numero_vendedor': '3228901235', 'clics_carrito': 37},
    {'nombre': 'Crema de Leche', 'descripcion': 'Crema de leche espesa para cocinar. Frasco 300ml.', 'precio': 7000, 'stock': 45, 'categoria': 'Lácteos', 'marca': 'Lácteos del Campo', 'numero_vendedor': '3229012346', 'clics_carrito': 25},
    {'nombre': 'Queso Parmesano Rallado', 'descripcion': 'Queso parmesano rallado importado. Frasco 200g.', 'precio': 18000, 'stock': 28, 'categoria': 'Lácteos', 'marca': 'Parmigiano', 'numero_vendedor': '3230123457', 'clics_carrito': 19},
    {'nombre': 'Leche Entera', 'descripcion': 'Leche entera pasteurizada. Cartón de 1L.', 'precio': 5000, 'stock': 60, 'categoria': 'Lácteos', 'marca': 'Leche Fresca', 'numero_vendedor': '3231234568', 'clics_carrito': 41},
    {'nombre': 'Queso Crema', 'descripcion': 'Queso crema para untar. Envase de 250g.', 'precio': 8500, 'stock': 38, 'categoria': 'Lácteos', 'marca': 'Cream Cheese', 'numero_vendedor': '3232345679', 'clics_carrito': 28},
    {'nombre': 'Kéfir Natural', 'descripcion': 'Kéfir probiótico natural. Botella de 500ml.', 'precio': 11000, 'stock': 30, 'categoria': 'Lácteos', 'marca': 'Probiotics Plus', 'numero_vendedor': '3233456780', 'clics_carrito': 16},
    {'nombre': 'Ricotta Fresca', 'descripcion': 'Queso ricotta fresco para postres. Envase 300g.', 'precio': 13000, 'stock': 25, 'categoria': 'Lácteos', 'marca': 'Quesos Finos', 'numero_vendedor': '3234567891', 'clics_carrito': 18},
    {'nombre': 'Suero Costeño', 'descripcion': 'Suero atollabuey costeño tradicional. Botella 500ml.', 'precio': 6500, 'stock': 42, 'categoria': 'Lácteos', 'marca': 'Lácteos Costeños', 'numero_vendedor': '3235678902', 'clics_carrito': 32},
    
    # Carnes y Embutidos (8)
    {'nombre': 'Chorizo Parrillero', 'descripcion': 'Chorizo argentino para parrilla. Paquete de 4 unidades.', 'precio': 16000, 'stock': 30, 'categoria': 'Carnes', 'marca': 'Carnes Premium', 'numero_vendedor': '3236789013', 'clics_carrito': 29},
    {'nombre': 'Jamón Serrano', 'descripcion': 'Jamón serrano curado importado. Paquete 200g.', 'precio': 22000, 'stock': 20, 'categoria': 'Carnes', 'marca': 'Ibéricos', 'numero_vendedor': '3237890124', 'clics_carrito': 14},
    {'nombre': 'Salami Italiano', 'descripcion': 'Salami italiano artesanal. Pieza de 300g.', 'precio': 18000, 'stock': 25, 'categoria': 'Carnes', 'marca': 'Salumi Italiani', 'numero_vendedor': '3238901235', 'clics_carrito': 21},
    {'nombre': 'Butifarra', 'descripcion': 'Butifarra catalana tradicional. Paquete de 6.', 'precio': 14000, 'stock': 32, 'categoria': 'Carnes', 'marca': 'Embutidos Catalanes', 'numero_vendedor': '3239012346', 'clics_carrito': 17},
    {'nombre': 'Pechuga de Pollo Ahumada', 'descripcion': 'Pechuga ahumada rebanada. Paquete 250g.', 'precio': 15000, 'stock': 35, 'categoria': 'Carnes', 'marca': 'Pollo Gourmet', 'numero_vendedor': '3240123457', 'clics_carrito': 26},
    {'nombre': 'Mortadela con Aceitunas', 'descripcion': 'Mortadela con aceitunas. Paquete 300g.', 'precio': 10000, 'stock': 40, 'categoria': 'Carnes', 'marca': 'Embutidos Tradicionales', 'numero_vendedor': '3241234568', 'clics_carrito': 23},
    {'nombre': 'Tocino Ahumado', 'descripcion': 'Tocino ahumado en tiras. Paquete 250g.', 'precio': 13000, 'stock': 38, 'categoria': 'Carnes', 'marca': 'Bacon Premium', 'numero_vendedor': '3242345679', 'clics_carrito': 31},
    {'nombre': 'Longaniza', 'descripcion': 'Longaniza colombiana tradicional. Paquete 500g.', 'precio': 17000, 'stock': 28, 'categoria': 'Carnes', 'marca': 'Carnes del Valle', 'numero_vendedor': '3243456780', 'clics_carrito': 20},
    
    # Snacks y Dulces (12)
    {'nombre': 'Papas Fritas Naturales', 'descripcion': 'Chips de papa natural sin freír. Bolsa 150g.', 'precio': 5500, 'stock': 60, 'categoria': 'Snacks', 'marca': 'Chips Saludables', 'numero_vendedor': '3244567891', 'clics_carrito': 44},
    {'nombre': 'Maní Garrapiñado', 'descripcion': 'Maní recubierto de azúcar caramelizada. Bolsa 200g.', 'precio': 6000, 'stock': 55, 'categoria': 'Snacks', 'marca': 'Dulces Caseros', 'numero_vendedor': '3245678902', 'clics_carrito': 35},
    {'nombre': 'Palomitas de Maíz Gourmet', 'descripcion': 'Palomitas con mantequilla y sal marina. Bolsa 250g.', 'precio': 8000, 'stock': 48, 'categoria': 'Snacks', 'marca': 'Popcorn Pro', 'numero_vendedor': '3246789013', 'clics_carrito': 40},
    {'nombre': 'Mix de Frutos Secos', 'descripcion': 'Mezcla de nueces, almendras y pasas. Bolsa 300g.', 'precio': 16000, 'stock': 35, 'categoria': 'Snacks', 'marca': 'Nuts & More', 'numero_vendedor': '3247890124', 'clics_carrito': 27},
    {'nombre': 'Chocolatinas Artesanales', 'descripcion': 'Bombones de chocolate rellenos. Caja de 12.', 'precio': 19000, 'stock': 30, 'categoria': 'Dulces', 'marca': 'Choco Boutique', 'numero_vendedor': '3248901235', 'clics_carrito': 24},
    {'nombre': 'Caramelos de Miel', 'descripcion': 'Caramelos naturales con miel de abejas. Bolsa 150g.', 'precio': 4500, 'stock': 50, 'categoria': 'Dulces', 'marca': 'Dulces Naturales', 'numero_vendedor': '3249012346', 'clics_carrito': 18},
    {'nombre': 'Turrones de Almendra', 'descripcion': 'Turrones españoles con almendra. Barra 200g.', 'precio': 12000, 'stock': 25, 'categoria': 'Dulces', 'marca': 'Turrones Españoles', 'numero_vendedor': '3250123457', 'clics_carrito': 15},
    {'nombre': 'Marshmallows Artesanales', 'descripcion': 'Malvaviscos caseros de vainilla. Bolsa 200g.', 'precio': 7000, 'stock': 42, 'categoria': 'Dulces', 'marca': 'Sweet Cloud', 'numero_vendedor': '3251234568', 'clics_carrito': 22},
    {'nombre': 'Gomitas de Fruta Natural', 'descripcion': 'Gomitas sin colorantes artificiales. Bolsa 250g.', 'precio': 8500, 'stock': 45, 'categoria': 'Dulces', 'marca': 'Gummy Natural', 'numero_vendedor': '3252345679', 'clics_carrito': 33},
    {'nombre': 'Pretzels Salados', 'descripcion': 'Pretzels tradicionales con sal gruesa. Bolsa 300g.', 'precio': 6500, 'stock': 40, 'categoria': 'Snacks', 'marca': 'Pretzel House', 'numero_vendedor': '3253456780', 'clics_carrito': 28},
    {'nombre': 'Nachos con Queso', 'descripcion': 'Nachos tostados con salsa de queso. Paquete 350g.', 'precio': 11000, 'stock': 38, 'categoria': 'Snacks', 'marca': 'Nacho King', 'numero_vendedor': '3254567891', 'clics_carrito': 36},
    {'nombre': 'Barritas Energéticas', 'descripcion': 'Barritas de cereales y miel. Caja de 6.', 'precio': 13000, 'stock': 32, 'categoria': 'Snacks', 'marca': 'Energy Bars', 'numero_vendedor': '3255678902', 'clics_carrito': 25},
    
    # Alimentos Preparados (10)
    {'nombre': 'Lasaña Congelada', 'descripcion': 'Lasaña de carne lista para hornear. Porción 400g.', 'precio': 18000, 'stock': 25, 'categoria': 'Alimentos', 'marca': 'Comida Lista', 'numero_vendedor': '3256789013', 'clics_carrito': 30},
    {'nombre': 'Tamales Colombianos', 'descripcion': 'Tamales tradicionales tolimenses. Paquete de 3.', 'precio': 21000, 'stock': 20, 'categoria': 'Alimentos', 'marca': 'Tamales Tolima', 'numero_vendedor': '3257890124', 'clics_carrito': 26},
    {'nombre': 'Pizza Congelada', 'descripcion': 'Pizza margarita lista para hornear. Tamaño familiar.', 'precio': 22000, 'stock': 30, 'categoria': 'Alimentos', 'marca': 'Pizza Express', 'numero_vendedor': '3258901235', 'clics_carrito': 38},
    {'nombre': 'Sopas Instantáneas', 'descripcion': 'Sopa de pollo lista en 3 minutos. Paquete de 5.', 'precio': 12000, 'stock': 50, 'categoria': 'Alimentos', 'marca': 'Sopa Rápida', 'numero_vendedor': '3259012346', 'clics_carrito': 34},
    {'nombre': 'Hummus de Garbanzo', 'descripcion': 'Hummus casero de garbanzos. Envase 300g.', 'precio': 10000, 'stock': 35, 'categoria': 'Alimentos', 'marca': 'Mediterranean Food', 'numero_vendedor': '3260123457', 'clics_carrito': 21},
    {'nombre': 'Guacamole Fresco', 'descripcion': 'Guacamole preparado con aguacate hass. 250g.', 'precio': 11000, 'stock': 28, 'categoria': 'Alimentos', 'marca': 'Avocado Fresh', 'numero_vendedor': '3261234568', 'clics_carrito': 29},
    {'nombre': 'Salsa de Tomate Casera', 'descripcion': 'Salsa de tomate artesanal para pasta. Frasco 500ml.', 'precio': 9000, 'stock': 40, 'categoria': 'Alimentos', 'marca': 'Salsa Italiana', 'numero_vendedor': '3262345679', 'clics_carrito': 23},
    {'nombre': 'Ceviche de Pescado', 'descripcion': 'Ceviche peruano fresco para consumir. Porción 300g.', 'precio': 16000, 'stock': 15, 'categoria': 'Alimentos', 'marca': 'Mar Fresco', 'numero_vendedor': '3263456780', 'clics_carrito': 19},
    {'nombre': 'Falafel Congelado', 'descripcion': 'Falafel vegano listo para freír. Paquete de 10.', 'precio': 13000, 'stock': 32, 'categoria': 'Alimentos', 'marca': 'Veggie World', 'numero_vendedor': '3264567891', 'clics_carrito': 17},
    {'nombre': 'Arroz Preparado', 'descripcion': 'Arroz con vegetales listo para calentar. 400g.', 'precio': 8000, 'stock': 45, 'categoria': 'Alimentos', 'marca': 'Rice & Go', 'numero_vendedor': '3265678902', 'clics_carrito': 27},
    
    # Condimentos y Especias (8)
    {'nombre': 'Aceite de Coco', 'descripcion': 'Aceite de coco virgen extra. Frasco 500ml.', 'precio': 18000, 'stock': 30, 'categoria': 'Condimentos', 'marca': 'Coco Oil', 'numero_vendedor': '3266789013', 'clics_carrito': 20},
    {'nombre': 'Miel de Maple', 'descripcion': 'Jarabe de arce canadiense puro. Botella 250ml.', 'precio': 24000, 'stock': 20, 'categoria': 'Condimentos', 'marca': 'Maple Canada', 'numero_vendedor': '3267890124', 'clics_carrito': 16},
    {'nombre': 'Salsa BBQ Ahumada', 'descripcion': 'Salsa barbacoa con sabor ahumado. Frasco 400ml.', 'precio': 10000, 'stock': 38, 'categoria': 'Condimentos', 'marca': 'BBQ Master', 'numero_vendedor': '3268901235', 'clics_carrito': 31},
    {'nombre': 'Vinagre Balsámico', 'descripcion': 'Vinagre balsámico de Módena. Botella 250ml.', 'precio': 15000, 'stock': 25, 'categoria': 'Condimentos', 'marca': 'Balsamic Italia', 'numero_vendedor': '3269012346', 'clics_carrito': 18},
    {'nombre': 'Mostaza Dijon', 'descripcion': 'Mostaza francesa Dijon. Frasco 200g.', 'precio': 8500, 'stock': 35, 'categoria': 'Condimentos', 'marca': 'Moutarde de Dijon', 'numero_vendedor': '3270123457', 'clics_carrito': 22},
    {'nombre': 'Salsa de Soya Premium', 'descripcion': 'Salsa de soya naturalmente fermentada. Botella 500ml.', 'precio': 12000, 'stock': 40, 'categoria': 'Condimentos', 'marca': 'Asian Sauce', 'numero_vendedor': '3271234568', 'clics_carrito': 28},
    {'nombre': 'Pesto de Albahaca', 'descripcion': 'Pesto italiano con albahaca fresca. Frasco 200g.', 'precio': 14000, 'stock': 28, 'categoria': 'Condimentos', 'marca': 'Pesto Genovese', 'numero_vendedor': '3272345679', 'clics_carrito': 24},
    {'nombre': 'Especias para Paella', 'descripcion': 'Mezcla de especias para paella española. Frasco 100g.', 'precio': 9000, 'stock': 32, 'categoria': 'Condimentos', 'marca': 'Especias España', 'numero_vendedor': '3273456780', 'clics_carrito': 15},
    
    # Vegetales y Verduras (6)
    {'nombre': 'Ensalada Pre-lavada', 'descripcion': 'Mix de lechugas listo para consumir. Bolsa 200g.', 'precio': 5500, 'stock': 40, 'categoria': 'Vegetales', 'marca': 'Fresh Greens', 'numero_vendedor': '3274567891', 'clics_carrito': 26},
    {'nombre': 'Aguacate Hass', 'descripcion': 'Aguacate hass maduro listo para consumir. 3 unidades.', 'precio': 8000, 'stock': 50, 'categoria': 'Vegetales', 'marca': 'Aguacates Premium', 'numero_vendedor': '3275678902', 'clics_carrito': 39},
    {'nombre': 'Tomates Cherry', 'descripcion': 'Tomates cherry dulces. Bandeja 250g.', 'precio': 6000, 'stock': 45, 'categoria': 'Vegetales', 'marca': 'Tomates Frescos', 'numero_vendedor': '3276789013', 'clics_carrito': 32},
    {'nombre': 'Champiñones Portobello', 'descripcion': 'Champiñones portobello frescos. Bandeja 300g.', 'precio': 9000, 'stock': 30, 'categoria': 'Vegetales', 'marca': 'Hongos Gourmet', 'numero_vendedor': '3277890124', 'clics_carrito': 21},
    {'nombre': 'Espárragos Verdes', 'descripcion': 'Espárragos verdes frescos. Manojo 250g.', 'precio': 12000, 'stock': 25, 'categoria': 'Vegetales', 'marca': 'Vegetales Premium', 'numero_vendedor': '3278901235', 'clics_carrito': 17},
    {'nombre': 'Brócoli Fresco', 'descripcion': 'Brócoli verde fresco. Unidad aproximada 500g.', 'precio': 5000, 'stock': 35, 'categoria': 'Vegetales', 'marca': 'Verduras del Campo', 'numero_vendedor': '3279012346', 'clics_carrito': 23}
]

print("🚀 Iniciando población de productos...")
print("="*60)

productos_creados = 0
productos_con_imagen = 0
errores = 0

for idx, producto_data in enumerate(productos_adicionales, start=1):
    try:
        # Crear o obtener producto
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
            print(f"✅ [{idx}/79] Producto creado: {producto.nombre}")
            
            # Intentar descargar y agregar imagen
            try:
                # Usar seed único basado en el nombre del producto para consistencia
                seed = abs(hash(producto.nombre)) % 10000
                image_url = get_product_image_url(seed)
                
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    # Crear nombre de archivo único
                    filename = f"producto_{producto.id}_{seed}.jpg"
                    
                    # Crear ImagenProducto
                    imagen = ImagenProducto(producto=producto)
                    imagen.imagen.save(
                        filename,
                        ContentFile(response.content),
                        save=True
                    )
                    productos_con_imagen += 1
                    print(f"   📸 Imagen agregada para: {producto.nombre}")
                else:
                    print(f"   ⚠️ No se pudo descargar imagen para: {producto.nombre}")
            except Exception as e:
                print(f"   ⚠️ Error al agregar imagen para {producto.nombre}: {str(e)}")
        else:
            print(f"ℹ️ [{idx}/79] Producto ya existe: {producto.nombre}")
            
    except Exception as e:
        errores += 1
        print(f"❌ Error al crear producto {producto_data['nombre']}: {str(e)}")

print("\n" + "="*60)
print(f"📊 RESUMEN FINAL:")
print(f"   ✅ Productos nuevos creados: {productos_creados}")
print(f"   📸 Productos con imagen: {productos_con_imagen}")
print(f"   ❌ Errores encontrados: {errores}")
print(f"   📦 Total de productos en la BD: {Producto.objects.count()}")
print("="*60)
print("\n🎉 ¡Proceso completado!")
