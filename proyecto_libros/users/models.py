from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

#todo:esta funcion ya se usa en otro lado, deberia poder reutilizarse
def user_image_directory_path(instance, filename):
    # Construye la ruta de la imagen con el ISBN
    return os.path.join('avatars', str(instance.user.username), filename)

class Imagen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=user_image_directory_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.imagen}"