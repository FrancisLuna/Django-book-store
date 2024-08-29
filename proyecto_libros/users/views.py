from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import DetailView, DeleteView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from users.forms import UserEditForm, UserRegisterForm

from .models import Imagen

# Create your views here.
def login_request(request):
    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contrasenia)
            if user is not None:
                login(request, user)
                next_url = request.GET.get("next", "/")
                return HttpResponseRedirect(next_url)
        msg_login = "Usuario o contraseña incorrectos"
    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form, "msg_login": msg_login})

# Vista de registro
def register(request):
    msg_register = ""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Si los datos ingresados en el form son válidos, con form.save() creamos un nuevo user usando esos datos
            user = form.save()
            # Obtener el archivo de imagen si existe
            image = request.FILES.get('imagen')
            # Crear una instancia del modelo Imagen
            Imagen.objects.create(user=user, imagen=image)
            return render(request, "mi_app/index.html")
        else:
            msg_register = "Error en los datos ingresados"
    else:
        form = UserRegisterForm()
    return render(request, "users/registro.html", {"form": form, "msg_register": msg_register})
# Vista de editar el perfil
# Obligamos a loguearse para editar los datos del usuario
@login_required
def editar_perfil(request):
    # El usuario para poder editar su perfil primero debe estar logueado.
    # Al estar logueado, podremos encontrar dentro del request la instancia
    # del usuario -> request.user
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES, instance=usuario)
        if miFormulario.is_valid():
            print(miFormulario.cleaned_data)
            if miFormulario.cleaned_data.get('imagen'):
                usuario.imagen.imagen = miFormulario.cleaned_data.get('imagen')
                usuario.imagen.save()
            miFormulario.save()

            return render(request, "mi_app/index.html")

    else:
        miFormulario = UserEditForm(instance=usuario)

    return render(request, "users/editar_usuario.html", {"mi_form": miFormulario, "usuario": usuario})

class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/editar_pass.html"
    success_url = reverse_lazy("EditarPerfil")

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'user_detail'

    def get_object(self):
        # Retorna el usuario logueado
        return self.request.user

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        # Retorna el usuario logueado
        return self.request.user
