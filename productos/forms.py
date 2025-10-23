from django import forms
from .models import Producto, ImagenProducto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'marca', 'stock']

class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenProducto
        fields = ['imagen']

ImagenProductoFormSet = forms.modelformset_factory(
    ImagenProducto,
    form=ImagenProductoForm,
    extra=3,  # número de campos de imagen por defecto
)
