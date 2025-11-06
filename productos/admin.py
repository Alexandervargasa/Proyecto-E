from django.contrib import admin
from .models import Producto, ImagenProducto

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ('imagen',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria', 'marca', 'clics_carrito', 'numero_vendedor', 'fecha_registro')
    list_filter = ('categoria', 'marca', 'fecha_registro')
    search_fields = ('nombre', 'descripcion', 'marca', 'categoria')
    readonly_fields = ('clics_carrito', 'fecha_registro')
    inlines = [ImagenProductoInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'precio', 'stock')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'marca')
        }),
        ('Contacto', {
            'fields': ('numero_vendedor',)
        }),
        ('Estadísticas', {
            'fields': ('clics_carrito', 'fecha_registro'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'imagen')
    list_filter = ('producto',)
