from django.urls import path
from . import views
from django.urls import re_path as url

from .views import OrderedProductsByUserListView, AllClientsForEmployeeView, client_list, EmployeeListView, \
    ReviewListView, ReviewCreateView, ClientsGroupedByCityView, LogoutView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^products/$', views.ProductListView.as_view(), name='products'),
    url(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product-detail'),
    url(r'^manufacturers/$', views.ManufacturerListView.as_view(), name='manufacturers'),
    url(r'^manufacturer/(?P<pk>\d+)$', views.ManufacturerDetailView.as_view(), name='manufacturer-detail'),

    # path('books/', views.BookListView.as_view(), name='books'),
]

urlpatterns += [
    url(r'^my-orders/$', views.OrdersByUserListView.as_view(), name='my-orders'),
]

urlpatterns += [
    url(r'^all-orders/$', views.AllOrdersForEmployeeView.as_view(), name='all-orders'),
]

urlpatterns += [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('order/<uuid:order_id>/', OrderedProductsByUserListView.as_view(), name='order-detail'),
]
urlpatterns += [
    url(r'^order/(?P<pk>[-\w]+)/change-status/$', views.change_status_employee, name='change-status-employee'),
    ]

urlpatterns += [url(r'^cart/$', views.CartView.as_view(), name='cart'),
                ]
urlpatterns += [url('create-order/', views.create_order, name='create-order'),
                url(r'^increase-quantity/(?P<product_instance_id>[0-9a-f-]+)/$', views.increase_quantity,
                            name='increase-quantity'),
                url(r'^decrease-quantity/(?P<product_instance_id>[0-9a-f-]+)/$', views.decrease_quantity,
                            name='decrease-quantity'),
                url(r'^remove-from-cart/(?P<product_instance_id>[0-9a-f-]+)/$', views.remove_from_cart,
                            name='remove-from-cart'),
                path('onlineshop/cart/apply-promo-code/', views.apply_promo_code, name='apply-promo-code'),
                path('promo-codes/', views.PromoCodeListView.as_view(), name='promo-codes'),
                path('clients/all/', views.AllClientsForEmployeeView.as_view(), name='all-clients'),
                path('clients/', views.client_list, name='clients'),
                path('contacts/', EmployeeListView.as_view(), name='contacts'),
                path('reviews/', ReviewListView.as_view(), name='reviews'),
                path('reviews/add/', ReviewCreateView.as_view(), name='add-review'),
                path('clients_grouped_by_city/', ClientsGroupedByCityView.as_view() , name='clients_grouped_by_city'),
]

urlpatterns += [
    path('logout/', LogoutView.as_view(), name='logout'),
]

