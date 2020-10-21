from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='index'),
    path('cart/', views.cart_page, name='cart'),
    path('about/', views.about_page, name='about'),
    path('shop/category/<int:pk>/', views.product_page, name='product'),
    path('shop/product/<int:pk>', views.product_detail_page, name='product_detail'),
    path('shop/product/addcard', views.addCart, name='add_cart'),
    path('shop/product/delete', views.delete_item, name='delete_item'),
    path('shop/product/modify', views.changeAmount, name='modify'),
    path('shop/product/add_comment', views.add_comment, name='add_comment'),

]
