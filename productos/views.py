from django.shortcuts import render, redirect
from .models import Producto, ImagenProducto
from .forms import ProductoForm
from django.forms import modelformset_factory


def discover(request):
    productos = Producto.objects.prefetch_related('imagenes').all()
    return render(request, 'discover.html', {'productos': productos})
def agregar_producto(request):
    ImagenFormSet = modelformset_factory(ImagenProducto, fields=('imagen',), extra=3)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # <-- Agregado request.FILES
        formset = ImagenFormSet(request.POST, request.FILES, queryset=ImagenProducto.objects.none())

        if form.is_valid() and formset.is_valid():
            producto = form.save()

            for imagen_form in formset.cleaned_data:
                if imagen_form:
                    ImagenProducto.objects.create(
                        producto=producto,
                        imagen=imagen_form['imagen']
                    )

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
