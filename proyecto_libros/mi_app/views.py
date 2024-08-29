from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.views import View

from django.db.models import Q
from django.db import transaction

from .models import Libro, Order, OrderItem
from .forms import OrderForm, ProductForm, ProductImageFormSet



# Base
def index(request):
    return render(request, "mi_app/index.html")

def about(request):
    return render(request, "mi_app/about.html")

########################################################################################
# CRUD LIBROS
class LibroListView(ListView):
    model = Libro
    template_name = 'mi_app/libro/libro_list.html'
    context_object_name = 'libros'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'mi_app//libro/libro_detail.html'
    context_object_name = 'libro'

    def get_object(self):
        isbn = self.kwargs.get('isbn')
        return get_object_or_404(Libro, isbn=isbn)

class LibroCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Libro
    form_class = ProductForm
    template_name = 'mi_app//libro/libro_add.html'
    success_url = reverse_lazy('books_list')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProductImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = ProductImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class LibroUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Libro
    form_class = ProductForm
    template_name = 'mi_app//libro/libro_add.html'
    success_url = reverse_lazy('books_list')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = ProductImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_object(self):
        isbn = self.kwargs.get('isbn')
        return get_object_or_404(Libro, isbn=isbn)

class LibroDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Libro
    template_name = 'mi_app//libro/libro_confirm_delete.html'
    success_url = reverse_lazy('books_list')

    def test_func(self):
        return self.request.user.is_staff
    
    def get_object(self):
        isbn = self.kwargs.get('isbn')
        return get_object_or_404(Libro, isbn=isbn)

########################################################################################
# CRUD ORDERS

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'mi_app/order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Filtrar por usuario autenticado si no es staff
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(customer=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'mi_app/order/order_detail.html'
    context_object_name = 'order'  # Nombre del contexto para el objeto Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.object)  # Cambia el nombre del contexto a order_items
        return context

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'mi_app/order/update_order.html'
    success_url = reverse_lazy('order_list')

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'mi_app/order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

def order_confirmation(request, order_id):
    # Obtener la orden con el ID proporcionado
    order = get_object_or_404(Order, id=order_id)
    # Obtener los artículos de la orden
    order_items = OrderItem.objects.filter(order=order)
    
    return render(request, 'mi_app/order/order_confirmation.html', {
        'order': order,
        'order_items': order_items,
    })

class OrderCreateView(LoginRequiredMixin, View):
    template_name = 'mi_app/order/create_order.html'
    
    def get(self, request):
        # Crear un formulario vacío para la orden
        order_books_forms = [OrderForm()]
        # Obtener todos los libros disponibles
        libros = Libro.objects.all()

        return render(request, self.template_name, {
            'order_books_forms': order_books_forms,
            'libros': libros,
        })
    
    def post(self, request):
            # Obtener los datos de los libros y cantidades
            book_isbns = request.POST.getlist('book')
            quantities = request.POST.getlist('quantity')
            
            # Comprobar si las listas están vacías
            if not book_isbns or not quantities:
                # Manejar el caso donde no hay libros seleccionados
                return redirect('order_create')  # Redirigir a la página de creación de orden
            
            # Emparejar los ISBNs de los libros con las cantidades
            order_items_data = zip(book_isbns, quantities)
            
            # Obtener el usuario autenticado como el cliente
            customer = request.user
            
            # Iniciar una transacción atómica
            try:
                with transaction.atomic():
                    # Crear una nueva orden
                    order = Order.objects.create(customer=customer)
                    
                    # Crear cada artículo de orden
                    for product_isbn, quantity in order_items_data:
                        product = Libro.objects.get(isbn=product_isbn)
                        OrderItem.objects.create(order=order, product=product, quantity=quantity)
                
                # Redirigir a la confirmación de la orden
                return redirect('order_confirmation', order_id=order.id)
            
            except Libro.DoesNotExist:
                # Manejar el caso donde el libro no existe
                # Puedes añadir un mensaje de error si quieres
                return render(request, self.template_name, {
                    'error_message': 'Uno de los libros seleccionados no existe. Por favor, verifique y vuelva a intentarlo.',
                    'libros': Libro.objects.all(),
                    'order_books_forms': [OrderForm()],
                })
            
            except Exception as e:
                # Manejar cualquier otro error que pueda ocurrir
                error_type = type(e).__name__
                error_message = str(e)
                return render(request, self.template_name, {
                    'error_message': 'Ocurrió un problema al procesar su pedido. Por favor, póngase en contacto con el soporte.',
                    'error_details': f'Tipo de error: {error_type}, Mensaje: {error_message}',
                    'libros': Libro.objects.all(),
                    'order_books_forms': [OrderForm()],
                })



########################################################################################
# BUSCADOR
class BuscarLibroView(ListView):
    model = Libro
    template_name = 'mi_app/libro/libro_list.html'  # Puedes reutilizar la misma plantilla
    context_object_name = 'libros'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Libro.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        return Libro.objects.all()