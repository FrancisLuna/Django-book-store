from django.contrib import admin
from .models import Libro,Order,OrderItem,ProductImage

admin.site.register(Libro)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)