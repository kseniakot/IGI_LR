from django.contrib import admin
from .models import Employee, ProductType, Product, Client, Order, Manufacturer


# admin.site.register(Employee)
# admin.site.register(ProductType)
# admin.site.register(Product)
# admin.site.register(Client)
# admin.site.register(Order)
# admin.site.register(Manufacturer)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position')
    list_filter = ('position',)
    search_fields = ('first_name', 'last_name')


class ProductsInstanceInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductsInstanceInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'product_type', 'manufacturer')
    list_filter = ('price',)
    search_fields = ('name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'order_date')

    list_filter = ('order_date',)
    search_fields = ('client',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')
