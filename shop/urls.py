from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='index'),
    path('cart/', views.cart_page, name='cart'),
    path('about/', views.about_page, name='about'),
    path('product/', views.product_page, name='product'),
    path('shop/', views.shop_page, name='shop_page')

]