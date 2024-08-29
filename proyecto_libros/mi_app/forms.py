from django import forms
from .models import Libro, ProductImage, OrderItem

# LIBROS

class ProductForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['isbn', 'title', 'author', 'price', 'stock', 'description'] 

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

ProductImageFormSet = forms.inlineformset_factory(Libro, ProductImage, form=ProductImageForm, extra=10, max_num=10, min_num=1)

# ORDERS
class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class OrderQueryForm(forms.Form):
    order_number = forms.IntegerField(label="Número de Pedido", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de Pedido'}))
