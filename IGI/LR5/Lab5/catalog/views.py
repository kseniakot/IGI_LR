from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import FormView
from django.contrib.auth.models import Group
from .models import Product, Manufacturer, ProductInstance, Client, Order, ProductType, Cart
from .forms import RegisterForm


def index(request):
    """
        Функция отображения для домашней страницы сайта.

        """
    # Генерация "количеств" некоторых главных объектов
    num_products = Product.objects.all().count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Доступные продукты (статус = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_manufacturers = Manufacturer.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_products': num_products, 'num_manufacturers': num_manufacturers,
                 'num_visits': num_visits},
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    client = get_object_or_404(Client, user=request.user)
    product_instance, product_created = ProductInstance.objects.get_or_create(product=product, customer=client)
    cart, cart_created = Cart.objects.get_or_create(client=client)

    if not product_created:
        product_instance.quantity += 1
        product_instance.save()
    else:
        cart.products.add(product_instance)
    cart.update_total_price()
    cart.save()
    return redirect('products')


class RegisterView(FormView):
    model = User
    form_class = RegisterForm
    template_name = 'registration/sign_up.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()

        client = Client(user=user)
        client.save()
        return super().form_valid(form)


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        product_type_id = self.request.GET.get('product_type_id')
        manufacturer_id = self.request.GET.get('manufacturer_id')
        price_order = self.request.GET.get('price_order')
        if product_type_id:
            queryset = queryset.filter(product_type_id=product_type_id)
        if manufacturer_id:
            queryset = queryset.filter(manufacturer_id=manufacturer_id)
        if price_order == 'as77c':
            queryset = queryset.order_by('price')
        elif price_order == 'desc':
            queryset = queryset.order_by('-price')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = ProductType.objects.all()
        context['manufacturers'] = Manufacturer.objects.all()
        return context


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    model = Product


class ManufacturerDetailView(generic.DetailView):
    model = Manufacturer


class OrderedProductsByUserListView(LoginRequiredMixin, generic.ListView):
    model = ProductInstance
    template_name = 'catalog/order_detail.html'
    paginate_by = 10

    def get_queryset(self):
        self.order = get_object_or_404(Order, id=self.kwargs.get('order_id'), client__user=self.request.user)
        return self.order.products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        return context


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = Order
    template_name = 'catalog/orders_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(
            client__user=self.request.user)  # .filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import ProductInstance


class AllOrdersForEmployeeView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'catalog/all_orders.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employees').exists():
            return HttpResponseRedirect(reverse('index'))

        return super().dispatch(request, *args, **kwargs)


def get_queryset(self):
    return Order.objects.all()


from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .models import Order
from .forms import OrderStatusForm, RegisterForm


# @permission_required('catalog.product_instance.set_product_as_issued')
def change_status_employee(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    order = get_object_or_404(Order, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = OrderStatusForm(request.POST, instance=order)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # product_inst.status = form.cleaned_data['status']
            # product_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-orders'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'catalog/change_status_employee.html', {'form': form, 'order': order})
