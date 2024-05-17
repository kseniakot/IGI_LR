from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Product, Manufacturer, ProductInstance


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


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    model = Product


class ManufacturerDetailView(generic.DetailView):
    model = Manufacturer


class OrderedProductsByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = ProductInstance
    template_name = 'catalog/productinstance_list_ordered_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductInstance.objects.filter(
            customer=self.request.user)  # .filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import ProductInstance


class AllOrdersForEmployeeView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all orders, accessible only to employees.
    """
    model = ProductInstance
    template_name = 'catalog/productinstance_list_all_orders.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employees').exists():
            return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ProductInstance.objects.all()


from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .models import Order
from .forms import OrderStatusForm


#@permission_required('catalog.product_instance.set_product_as_issued')
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
