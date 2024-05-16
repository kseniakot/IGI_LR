from django.urls import path
from . import views
from django.urls import re_path as url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/$', views.ProductListView.as_view(), name='products'),
    url(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product-detail'),
    url(r'^manufacturers/$', views.ManufacturerListView.as_view(), name='manufacturers'),
    url(r'^manufacturer/(?P<pk>\d+)$', views.ManufacturerDetailView.as_view(), name='manufacturer-detail'),
    # path('books/', views.BookListView.as_view(), name='books'),
]
urlpatterns += [
    url(r'^myproducts/$', views.OrderedProductsByUserListView.as_view(), name='my-ordered'),
]