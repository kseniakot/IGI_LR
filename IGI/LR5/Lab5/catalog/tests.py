from unittest.mock import patch

from django.test import TestCase, RequestFactory

from django.test import TestCase
from .models import Product, ProductType, Review
from .views import get_random_joke, get_public_ip, privacy, CartView, PromoCodeListView, add_to_cart, create_order


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        ProductType.objects.create(name='Test Product Type')
        Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                               product_type=ProductType.objects.get(name='Test Product Type'))

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name(self):
        product = Product.objects.get(id=1)
        expected_object_name = product.name
        self.assertEqual(expected_object_name, str(product))


from django.contrib.auth.models import User, Group
from .models import Employee


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='testuser')
        Employee.objects.create(user=User.objects.get(username='testuser'), first_name='John', last_name='Doe',
                                position='Developer')

    def test_first_name_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_position_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field('position').verbose_name
        self.assertEqual(field_label, 'position')

    def test_first_name_max_length(self):
        employee = Employee.objects.get(id=1)
        max_length = employee._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_username(self):
        employee = Employee.objects.get(id=1)
        expected_object_name = employee.user.username
        self.assertEqual(expected_object_name, str(employee))

    def test_save_method(self):
        employee = Employee.objects.get(id=1)
        group_exists = Group.objects.filter(name='Employees').exists()
        self.assertTrue(group_exists)
        user_in_group = employee.user.groups.filter(name='Employees').exists()
        self.assertTrue(user_in_group)


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='testuser')
        Review.objects.create(user=User.objects.get(username='testuser'), rating=5, text='Great product!')

    def test_str_method(self):
        review = Review.objects.get(id=1)
        expected_object_name = f'{review.user}: {"*" * review.rating} {review.text}'
        self.assertEqual(expected_object_name, str(review))

    def test_get_rating_method(self):
        review = Review.objects.get(id=1)
        expected_rating = '*' * review.rating
        self.assertEqual(expected_rating, review.get_rating())


class ProductTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        ProductType.objects.create(name='Test Product Type')

    def test_str_method(self):
        product_type = ProductType.objects.get(id=1)
        expected_object_name = product_type.name
        self.assertEqual(expected_object_name, str(product_type))


from .models import Article, Client, OrderItem, ProductInstance, PromoCode, Order, Product


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Article.objects.create(title='Test Article', summary='Test Summary', content='Test Content')

    def test_str_method(self):
        article = Article.objects.get(id=1)
        expected_object_name = article.title
        self.assertEqual(expected_object_name, str(article))


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='testuser')
        Group.objects.create(name='Salon clients')
        Client.objects.create(user=User.objects.get(username='testuser'), first_name='John', last_name='Doe')

    def test_str_method(self):
        client = Client.objects.get(id=1)
        expected_object_name = client.user.username
        self.assertEqual(expected_object_name, str(client))


class OrderItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product_type = ProductType.objects.create(name='Test Product Type')
        Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                               product_type=product_type)
        Order.objects.create(client=Client.objects.get(id=1))
        OrderItem.objects.create(product=Product.objects.get(id=1), quantity=1, order=Order.objects.get(id=1))


def test_str_method(self):
    order_item = OrderItem.objects.get(id=1)
    expected_object_name = f"{order_item.product.name} x {order_item.quantity}"
    self.assertEqual(expected_object_name, str(order_item))


class PromoCodeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PromoCode.objects.create(code='TESTCODE', discount=10)

    def test_str_method(self):
        promo_code = PromoCode.objects.get(id=1)
        expected_object_name = promo_code.code
        self.assertEqual(expected_object_name, str(promo_code))


from django.test import TestCase
from .models import Cart, Manufacturer, CompanyInfo, FAQ, Job


class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='testuser')
        Group.objects.create(name='Salon clients')
        Client.objects.create(user=User.objects.get(username='testuser'), first_name='John', last_name='Doe')
        Cart.objects.create(client=Client.objects.get(user__username='testuser'), total_price=100.00)

    def test_client_label(self):
        cart = Cart.objects.get(id=1)
        field_label = cart._meta.get_field('client').verbose_name
        self.assertEqual(field_label, 'client')

    # Add more tests for other Cart fields here


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name='Test Manufacturer', phone='1234567890', email='test@example.com')

    def test_name_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_phone_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'phone')

    def test_email_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_str_method(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = manufacturer.name
        self.assertEqual(expected_object_name, str(manufacturer))


class CompanyInfoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CompanyInfo.objects.create(text='Test Text')

    def test_text_label(self):
        companyinfo = CompanyInfo.objects.get(id=1)
        field_label = companyinfo._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')


class FAQModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        FAQ.objects.create(question='Test Question', answer='Test Answer')

    def test_question_label(self):
        faq = FAQ.objects.get(id=1)
        field_label = faq._meta.get_field('question').verbose_name
        self.assertEqual(field_label, 'question')


class JobModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Job.objects.create(title='Test Job', description='Test Description')

    def test_title_label(self):
        job = Job.objects.get(id=1)
        field_label = job._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')


class PrivacyViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_privacy_view(self):
        request = self.factory.get('/privacy/')
        response = privacy(request)
        self.assertEqual(response.status_code, 200)


class GetRandomJokeTest(TestCase):
    @patch('requests.get')
    def test_get_random_joke(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'setup': 'Why did the chicken cross the road?',
                                                   'punchline': 'To get to the other side.'}
        joke = get_random_joke()
        self.assertEqual(joke, 'Why did the chicken cross the road? - To get to the other side.')


class GetPublicIPTest(TestCase):
    @patch('requests.get')
    def test_get_public_ip(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'ip': '192.168.1.1'}
        ip = get_public_ip()
        self.assertEqual(ip, '192.168.1.1')


from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from django.urls import reverse
from unittest.mock import patch
from .views import change_status_employee
from .models import PromoCode, Order, Cart, Client


class PromoCodeListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_promo_code_list_view(self):
        PromoCode.objects.create(code='TESTCODE', discount=10)
        request = self.factory.get('/promo-codes/')
        response = PromoCodeListView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class ChangeStatusEmployeeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group.objects.create(name='Employees')
        self.user.groups.add(self.group)
        self.client.login(username='testuser', password='12345')
        Group.objects.create(name='Salon clients')  # Create the 'Salon clients' group
        self.client_obj = Client.objects.create(user=self.user, first_name='John', last_name='Doe')
        self.order = Order.objects.create(client=self.client_obj)

    @patch('django.shortcuts.get_object_or_404')
    def test_change_status_employee_view(self, mock_get):
        mock_get.return_value = self.order
        request = self.factory.post('/change-status-employee/')
        request.user = self.user
        response = change_status_employee(request, pk=self.order.pk)
        self.assertEqual(response.status_code, 302)


class CartViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        Group.objects.create(name='Salon clients')  # Create the 'Salon clients' group
        self.client_obj = Client.objects.create(user=self.user, first_name='John', last_name='Doe')
        self.cart = Cart.objects.create(client=self.client_obj)

    def test_cart_view(self):
        request = self.factory.get('/cart/')
        request.user = self.user
        response = CartView.as_view()(request)
        self.assertEqual(response.status_code, 200)


from django.test import TestCase
from .forms import ReviewForm
from .models import Review


class ReviewFormTest(TestCase):
    def test_review_form_valid(self):
        form = ReviewForm(data={'rating': '5', 'text': 'Great product!'})
        self.assertTrue(form.is_valid())

    def test_review_form_invalid(self):
        form = ReviewForm(data={'rating': '', 'text': 'Great product!'})
        self.assertFalse(form.is_valid())


from django.test import TestCase
from django.utils import timezone
from catalog.views import get_user_time


class GetUserTimeTest(TestCase):
    def test_get_user_time(self):
        user_time_data = get_user_time()
        current_time = timezone.localtime(timezone.now())
        expected_user_time_data = {
            "user_timezone": str(timezone.get_current_timezone()),
            "current_date_formatted": current_time.strftime("%d/%m/%Y %H:%M:%S"),
            "calendar_text": current_time.strftime("%B %Y"),
        }
        self.assertEqual(user_time_data, expected_user_time_data)


class OrderModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='jane', password='doe')
        Group.objects.create(name='Salon clients')
        client = Client.objects.create(user=user, first_name='Jane', last_name='Doe')
        product_type = ProductType.objects.create(name='Test Type')
        product = Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                                         product_type=product_type)
        product_instance = ProductInstance.objects.create(product=product, quantity=1)
        cls.order = Order.objects.create(client=client, total_price=10.00)
        cls.order.products.add(product_instance)
        cls.order.total_price = sum(item.product.price * item.quantity for item in cls.order.products.all())
        cls.order.save()

    def test_total_price_label(self):
        field_label = self.order._meta.get_field('total_price').verbose_name
        self.assertEqual(field_label, 'total price')

    def test_total_price_value(self):
        self.assertEqual(self.order.total_price, 10.00)


from django.urls import reverse
from catalog.views import ReviewListView
from catalog.models import Review


class ReviewListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_review_list_view(self):
        # Create a user
        user = User.objects.create_user(username='jane', password='doe')
        # Create a review associated with the user
        Review.objects.create(user=user, text='Test Review', rating=5)

        request = self.factory.get(reverse('reviews'))
        response = ReviewListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 1)


from unittest.mock import patch
from catalog.views import get_random_joke, get_public_ip


class GetPublicIpTest(TestCase):
    @patch('requests.get')
    def test_get_public_ip(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'ip': '123.123.123.123'}

        ip = get_public_ip()
        self.assertEqual(ip, '123.123.123.123')

    @patch('requests.get')
    def test_get_public_ip_failure(self, mock_get):
        mock_get.return_value.status_code = 404

        ip = get_public_ip()
        self.assertIsNone(ip)