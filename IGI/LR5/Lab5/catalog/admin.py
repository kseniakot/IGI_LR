from django.contrib import admin
from .models import Employee, ProductType, Product, Client, Order, Manufacturer, ProductInstance, Cart, PromoCode


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
    list_display = ('client', 'order_date', 'status', 'total_price', 'display_products')
    readonly_fields = ('total_price',)
    list_filter = ('order_date',)
    search_fields = ('client',)

    def display_products(self, obj):
        return ", ".join([str(product) for product in obj.products.all()])

    display_products.short_description = 'Products'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created i.e. it's an edit
            return self.readonly_fields + ('total_price',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.total_price = sum(product_instance.product.price for product_instance in obj.products.all())
        super().save_model(request, obj, form, change)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('client', 'total_price', 'display_products')
    readonly_fields = ('total_price',)
    search_fields = ('client',)

    def display_products(self, obj):
        return ", ".join([product.product.name for product in obj.products.all()])

    display_products.short_description = 'Products'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created i.e. it's an edit
            return self.readonly_fields + ('total_price',)
        return self.readonly_fields


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount')
    search_fields = ('code',)


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
