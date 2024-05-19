from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.models import User
import os
import logging
from django.db.models import Q, Count, Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.views.generic import ListView, View
from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView, CreateView
from .models import Product, Manufacturer, Client, ProductType, Cart, PromoCode, Employee, Review
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from .models import ProductInstance
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Order
from .forms import OrderStatusForm, RegisterForm, ReviewForm

log_level_name = os.getenv('LOG_LEVEL', 'DEBUG')
log_level = getattr(logging, log_level_name.upper(), logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

handler = logging.FileHandler('app.log')
handler.setLevel(log_level)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def privacy(request):
    logger.info('Executing privacy view')
    return render(request, 'catalog/privacy.html')


def get_random_joke():
    logger.debug('Executing get_random_joke function')
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} - {data['punchline']}"
    else:
        return None


def get_public_ip():
    logger.info('Executing get_public_ip function')
    response = requests.get('https://api.ipify.org?format=json')
    if response.status_code == 200:
        return response.json()['ip']
    else:
        return None


def index(request):
    logger.info('Executing index view')
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_products': Product.objects.count(),
        'num_manufacturers': Manufacturer.objects.count(),
        'num_visits': num_visits,
        'public_ip': get_public_ip(),
        'joke': get_random_joke(),
    }

    return render(request, 'index.html', context)


class RegisterView(FormView):
    logger.info('Executing RegisterView class')
    model = User
    form_class = RegisterForm
    template_name = 'registration/sign_up.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()

        dob = form.cleaned_data.get('date_of_birth')
        phone = form.cleaned_data.get('phone_number')
        city = form.cleaned_data.get('city')

        client = Client(user=user, date_of_birth=dob, phone_number=phone, city=city)
        client.save()

        return super().form_valid(form)


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10
    logger.info('Executing ProductListView class')

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


logger.info('Executing ManufacturerListView class')


class ProductDetailView(generic.DetailView):
    logger.info('Executing ProductDetailView class')
    model = Product


class ManufacturerDetailView(generic.DetailView):
    logger.info('Executing ManufacturerDetailView class')
    model = Manufacturer


class OrderedProductsByUserListView(LoginRequiredMixin, generic.ListView):
    model = ProductInstance
    logger.info('Executing OrderedProductsByUserListView class')
    template_name = 'catalog/order_detail.html'
    paginate_by = 10

    def get_queryset(self):
        logger.info('Executing get_queryset method')
        self.order = get_object_or_404(Order, id=self.kwargs.get('order_id'), client__user=self.request.user)
        return self.order.products.all()

    def get_context_data(self, **kwargs):
        logger.info('Executing get_context_data method')
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
    logger.info('Executing OrdersByUserListView class')

    def get_queryset(self):
        return Order.objects.filter(
            client__user=self.request.user).order_by('order_date')  # .filter(status__exact='o').order_by('due_back')


class AllOrdersForEmployeeView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'catalog/all_orders.html'
    paginate_by = 10
    logger.info('Executing AllOrdersForEmployeeView class')

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
    logger.info('Executing PromoCodeListView class')


# @permission_required('catalog.product_instance.set_product_as_issued')
def change_status_employee(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    logger.info('Executing change_status_employee view')
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
    logger.info('Executing CartView class')

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(client=self.request.user.client)
            print(cart.products.all())
            return cart


@login_required
def add_to_cart(request, product_id):
    logger.info('Executing add_to_cart view')
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
    logger.info('Executing create_order view')
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
    logger.info('Executing increase_quantity view')
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
        logger.exception('Invalid promo code')
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
    logger.info('Executing ReviewCreateView class')
    model = Review
    form_class = ReviewForm
    template_name = 'catalog/add_review.html'  # update this to your template
    success_url = '/catalog/reviews/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientsGroupedByCityView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        clients_with_orders = Client.objects.annotate(num_orders=Count('order')).filter(num_orders__gt=0)
        clients_list = clients_with_orders.values('city', 'user__username', 'num_orders').order_by('city')

        # Create a dictionary where each key is a city and the value is a list of clients in that city
        clients_grouped_by_city = {}
        for client in clients_list:
            if client['city'] in clients_grouped_by_city:
                clients_grouped_by_city[client['city']].append(client)
            else:
                clients_grouped_by_city[client['city']] = [client]

        most_demanded_product = Product.objects.annotate(total_quantity=Sum('productinstance__quantity')).order_by(
            '-total_quantity').first()

        no_demand_product = Product.objects.filter(productinstance__isnull=True)

        monthly_sales = Product.objects.filter(productinstance__order__isnull=False).annotate(
            month=ExtractMonth('productinstance__order__order_date'),
            year=ExtractYear('productinstance__order__order_date')
        ).values('month', 'year', 'product_type__name').annotate(
            total_quantity=Sum('productinstance__quantity')
        ).order_by('year', 'month', 'product_type__name')

        annual_sales = Order.objects.annotate(
            year=ExtractYear('order_date')
        ).values('year').annotate(
            total_revenue=Sum('total_price')
        ).order_by('year')

        return render(request, 'catalog/clients_grouped_by_cities.html', {
            'clients_grouped_by_city': clients_grouped_by_city,
            'most_demanded_product': most_demanded_product,
            'no_demand_product': no_demand_product,
            'monthly_sales': monthly_sales,
            'annual_sales': annual_sales,
        })


class LogoutView(View):
    logger.info('Executing LogoutView class')

    def get(self, request):
        logout(request)
        # logger.info(f'User logged out')
        return render(request, 'registration/logged_out.html')
