from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', views.register, name="Register"),
    path('login/', views.login_request, name="Login"),
    path('logout/', LogoutView.as_view(template_name='mi_app/index.html'), name="Logout"),
    path('edit/', views.editar_perfil, name="EditarPerfil"),
    path('profile/', views.UserDetailView.as_view(), name='user_detail'),
    path('delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('cambiar_pass/', views.CambiarContrasenia.as_view(), name="CambiarPass"),

]


