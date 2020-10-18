from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='index'),
    path('cart/', views.cart_page, name='cart'),
    path('about/', views.about_page, name='about'),
    path('shop/category/<int:pk>/', views.product_page, name='product'),
    path('shop/subcategory/<int:pk>/', views.product_subcat_page, name='product_subcat'),
    path('shop/product/<int:pk>', views.product_detail_page, name='product_detail'),
]