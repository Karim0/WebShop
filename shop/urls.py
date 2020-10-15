from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='index'),
    path('cart/', views.cart_page, name='cart'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('products/', views.product_page, name='products'),
    path('products_cat/<int:pk>', views.product_cat_page, name='products'),
    path('product_detail/<int:pk>', views.product_detail_page, name='product_detail'),
]