from django.urls import path
from mi_app import views

# Base
urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
]

# Libros
urlpatterns += [
    path('libros/', views.LibroListView.as_view(), name="books_list"),
    path('libros/create/', views.LibroCreateView.as_view(), name='book_create'),
    path('libros/<str:isbn>/', views.LibroDetailView.as_view(), name='book_isbn'),
    path('libros/<str:isbn>/update/', views.LibroUpdateView.as_view(), name='libro_update'),
    path('libros/<str:isbn>/delete/', views.LibroDeleteView.as_view(), name='libro_delete'),
]

# Buscador
urlpatterns += [
    path('buscar/', views.BuscarLibroView.as_view(), name='buscar_libro'),
]

# Orders
urlpatterns += [
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='update_order'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='delete_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
