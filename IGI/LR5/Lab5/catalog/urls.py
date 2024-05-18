from django.urls import path
from . import views
from django.urls import re_path as url

from .views import OrderedProductsByUserListView

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
urlpatterns += [url(r'^order/(?P<pk>[-\w]+)/change-status/$', views.change_status_employee, name='change-status-employee'),
]

