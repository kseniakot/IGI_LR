from django.shortcuts import render
from django.views import generic
from .models import Product, ProductType, Manufacturer, Order, Client


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
