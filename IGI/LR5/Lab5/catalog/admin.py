from django.contrib import admin
from .models import Employee, ProductType, Product, Client, Order, Manufacturer, ProductInstance


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
    list_display = ('user_username', 'first_name', 'last_name', 'user_email')
    search_fields = ('first_name', 'last_name')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'order_date')

    list_filter = ('order_date',)
    search_fields = ('client',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')


@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'customer', 'id')
    # list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('product', 'id')
        }),
        ('Info', {
            'fields': ('quantity', 'customer')
        }),
    )
