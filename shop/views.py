from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *


def home_page(request):
    content = {
        'pagename': 'Главная страница',
        'type': ''
    }
    return render(request, 'shop/index.html', content)


def cart_page(request):
    content = {
        'pagename': 'Корзина',
        'type': 'sub-head'
    }
    return render(request, 'shop/card-page.html', content)


def about_page(request):
    content = {
        'pagename': 'О компании',
        'type': 'sub-head'
    }
    return render(request, 'shop/about.html', content)


def product_page(request):
    content = {
        'pagename': 'Продукт',
        'type': 'sub-head'
    }
    return render(request, 'shop/product-details.html', content)


def shop_page(request):
    content = {
        'pagename': 'Категория',
        'type': 'sub-head'
    }
    return render(request, 'shop/shop.html', content)
