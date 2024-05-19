
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView, CreateView
from .models import Product, Manufacturer, Client, ProductType, Cart, PromoCode, Employee, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import ProductInstance
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Order
from .forms import OrderStatusForm, RegisterForm, ReviewForm


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
            client__user=self.request.user).order_by('order_date')  # .filter(status__exact='o').order_by('due_back')


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


class PromoCodeListView(generic.ListView):
    model = PromoCode
    template_name = 'catalog/promocode_list.html'
    paginate_by = 10


# @permission_required('catalog.product_instance.set_product_as_issued')
def change_status_employee(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    print(pk)
    order = get_object_or_404(Order, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = OrderStatusForm(request.POST, instance=order)

        # Check if the form is valid:
        if form.is_valid():
            order.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-orders'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'catalog/change_status_employee.html', {'form': form, 'order': order})


class CartView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'catalog/user_cart.html'

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(client=self.request.user.client)
            print(cart.products.all())
            return cart


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    client = get_object_or_404(Client, user=request.user)
    cart, cart_created = Cart.objects.get_or_create(client=client)
    cart.save()

    product_in_cart = cart.products.filter(
        product__name=product.name,
        product__manufacturer=product.manufacturer,
        product__price=product.price
    ).first()

    if not product_in_cart:
        # If there is no such product yet, create a new product instance
        product_instance = ProductInstance.objects.create(product=product, customer=client, quantity=1)
        cart.products.add(product_instance)
    else:
        product_in_cart.quantity += 1
        product_in_cart.save()
    cart.save()
    cart.update_total_price()  # Update the total price in the cart

    return redirect('products')


@login_required
def create_order(request):
    client = get_object_or_404(Client, user=request.user)
    cart = Cart.objects.get(client=client)  # Get the cart from the database again
    total_price = cart.total_price  # Save the total_price before clearing the cart
    promo_code = cart.promo_code  # Save the promo code before clearing the cart
    order = Order(client=client)
    order.total_price = total_price
    order.promo_code = promo_code
    print(promo_code)
    order.save()
    for product_instance in cart.products.all():
        order.products.add(product_instance)
    order.save()
    cart.products.clear()
    cart.update_total_price()  # Update the total_price in the cart after clearing the products
    cart.promo_code = None  # Clear the promo code in the cart
    cart.save()
    return redirect('my-orders')


@login_required
def increase_quantity(request, product_instance_id):
    product_instance = get_object_or_404(ProductInstance, id=product_instance_id)
    product_instance.quantity += 1
    product_instance.save()
    cart = get_object_or_404(Cart, client=request.user.client)
    cart.update_total_price()
    cart.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, product_instance_id):
    product_instance = get_object_or_404(ProductInstance, id=product_instance_id)
    if product_instance.quantity > 1:
        product_instance.quantity -= 1
        product_instance.save()
    cart = get_object_or_404(Cart, client=request.user.client)
    cart.update_total_price()
    cart.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, product_instance_id):
    product_instance = get_object_or_404(ProductInstance, id=product_instance_id)
    cart = get_object_or_404(Cart, client=request.user.client)
    cart.products.remove(product_instance)
    product_instance.delete()
    cart.update_total_price()
    cart.save()
    return redirect('cart')


def apply_promo_code(request):
    promo_code = request.POST.get('promo_code')
    try:
        promo = PromoCode.objects.get(code=promo_code)
        cart = Cart.objects.get(client=request.user.client)
        cart.promo_code = promo  # save the promo code in the cart
        cart.update_total_price()
        cart.save()
    # messages.success(request, 'Promo code applied successfully!')
    except PromoCode.DoesNotExist:
        pass
        # messages.error(request, 'Invalid promo code.')
    return redirect('cart')


class EmployeeListView(generic.ListView):
    model = Employee
    template_name = 'catalog/employee_list.html'


class AllClientsForEmployeeView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all clients, accessible only to employees.
    """
    model = User
    template_name = 'catalog/client_list_for_employee.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employees').exists():
            return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(groups__name='Shop Members').exclude(username='user').order_by('username')


def client_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        clients = Client.objects.filter(
            Q(user__username__istartswith=search_query) | Q(user__email__istartswith=search_query))
    else:
        clients = Client.objects.all().order_by('user__username')
    return render(request, 'catalog/client_list_for_employee.html', {'object_list': clients})


class ReviewListView(ListView):
    model = Review
    template_name = 'catalog/reviews.html'  # update this to your template


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'catalog/add_review.html'  # update this to your template
    success_url = '/catalog/reviews/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
