from datetime import datetime
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User, Group
import uuid


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='', null=True, blank=True)
    job_description = models.TextField(default='No description')
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(default='default@gmail.com')

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name='Employees')
        self.user.groups.add(group)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        stars = '*' * self.rating
        return f'{self.user}: {stars} {self.text}'

    def get_rating(self):
        return '*' * self.rating


class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('product-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    image = models.ImageField(upload_to='articles/')
    content = models.TextField()

    def __str__(self):
        return self.title


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, default='', blank=True)
    city = models.CharField(max_length=100, default='Minsk')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Salon clients')
        self.user.groups.add(group)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.user.username}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class ProductInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular product across whole shop")
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customer = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (("can_mark_issued", "Set product as issued"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id, self.product.name)

    @property
    def total_price(self):
        return self.product.price * self.quantity


class PromoCode(models.Model):
    code = models.CharField(max_length=10)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    # expiration_date = models.DateField(default=datetime.date(datetime.now()))

    def __str__(self):
        return self.code


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular order across whole shop")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInstance)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Processing'),
        ('s', 'Shipped'),
        ('d', 'Delivered'),
        ('i', 'Issued'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='p', help_text='Order status')

    def save(self, *args, **kwargs):
        self.total_price = sum(
            product_instance.product.price * product_instance.quantity for product_instance in self.products.all())
        if self.promo_code:
            self.total_price *= (1 - self.promo_code.discount / 100)
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        total_price = sum(
            product_instance.product.price * product_instance.quantity for product_instance in self.products.all())
        if self.promo_code:
            total_price *= (1 - self.promo_code.discount / 100)
        self.total_price = total_price
        self.save()

    def __str__(self):
        return f"Order {self.id} by {self.client}"


# @receiver(m2m_changed, sender=Order.products.through)
# def update_total_price(sender, instance, action, **kwargs):
#     if action == "post_add" or action == "post_remove":
#         instance.total_price = instance.calculate_total_price()
#         instance.save()


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInstance)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Cart for {self.client}"

    def update_total_price(self):
        total_price = sum(
            product_instance.product.price * product_instance.quantity for product_instance in self.products.all())
        if self.promo_code:
            total_price *= (1 - self.promo_code.discount / 100)
        self.total_price = total_price
        self.save()


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('manufacturer-detail', args=[str(self.id)])

    def __str__(self):
        return self.name
