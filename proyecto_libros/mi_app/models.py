from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.utils import timezone
import os

User = get_user_model()

# LIBROS
def product_image_directory_path(instance, filename):
    # Construye la ruta de la imagen con el ISBN
    return os.path.join('product_images', instance.product.isbn, filename)

class Libro(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = RichTextField(blank=True, null=True)  # Campo de texto enriquecido
    date_added = models.DateTimeField(default=timezone.now)  

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.title} by {self.author}"


class ProductImage(models.Model):
    product = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_directory_path)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

# ORDERS
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Libro, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Detalle del Pedido"
        verbose_name_plural = "Detalles del Pedido"

    def __str__(self):
        return f"{self.quantity} x {self.product.title} (Order #{self.order.id})"
