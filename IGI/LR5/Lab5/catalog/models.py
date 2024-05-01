from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.client}"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
