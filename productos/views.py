from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Producto, ImagenProducto
from .forms import ProductoForm
from django.forms import modelformset_factory


def discover(request):
    # Búsqueda de productos
    query = request.GET.get('q', '')
    
    if query:
        productos = Producto.objects.prefetch_related('imagenes').filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(marca__icontains=query) |
            Q(categoria__icontains=query)
        )
    else:
        productos = Producto.objects.prefetch_related('imagenes').all()
    
    return render(request, 'discover.html', {
        'productos': productos,
        'query': query
    })

def tendencias(request):
    # Productos más clickeados (top 10)
    productos = Producto.objects.prefetch_related('imagenes').filter(clics_carrito__gt=0).order_by('-clics_carrito')[:10]
    return render(request, 'tendencias.html', {'productos': productos})

@login_required
def agregar_al_carrito(request, producto_id):
    """Incrementa el contador de clics y devuelve el número del vendedor"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Incrementar contador
    producto.clics_carrito += 1
    producto.save()
    
    return JsonResponse({
        'success': True,
        'numero_vendedor': producto.numero_vendedor or 'No especificado',
        'nombre_producto': producto.nombre,
        'clics_totales': producto.clics_carrito
    })

@login_required
def agregar_producto(request):
    # Todos los usuarios autenticados pueden agregar productos
    ImagenFormSet = modelformset_factory(ImagenProducto, fields=('imagen',), extra=3)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        formset = ImagenFormSet(request.POST, request.FILES, queryset=ImagenProducto.objects.none())

        if form.is_valid() and formset.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user  # Asignar el producto al usuario actual
            producto.save()

            for imagen_form in formset.cleaned_data:
                if imagen_form:
                    ImagenProducto.objects.create(
                        producto=producto,
                        imagen=imagen_form['imagen']
                    )

            messages.success(request, "✅ Producto agregado exitosamente!")
            return redirect('discover')
        else:
            print("Errores en el formulario de producto:", form.errors)
            print("Errores en el formset de imágenes:", formset.errors)
    else:
        form = ProductoForm()
        formset = ImagenFormSet(queryset=ImagenProducto.objects.none())

    return render(request, 'AgregarProductos.html', {
        'form': form,
        'formset': formset
    })

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Verificar permisos:
    # - Admin (con perfil y rol='admin') puede eliminar cualquier producto
    # - Propietario puede eliminar solo sus propios productos
    # - Si el producto no tiene dueño (creado antes de la migración), solo admins pueden eliminarlo
    es_admin = hasattr(request.user, 'perfil') and request.user.perfil.es_admin()
    es_propietario = producto.usuario == request.user
    
    # Un admin puede eliminar cualquier cosa, o un usuario puede eliminar lo que es suyo
    if not (es_admin or es_propietario):
        messages.error(request, "❌ No tienes permisos para eliminar este producto. Solo puedes eliminar productos que tú hayas creado.")
        return redirect('discover')
    
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f"🗑️ El producto '{nombre_producto}' ha sido eliminado exitosamente.")
        return redirect('discover')
    
    return render(request, 'confirmar_eliminar.html', {'producto': producto})
