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

def product_page(request, pk):
    subcategory = Subcategory.objects.filter(category_id=pk)

    content = {
        'pagename': 'Продукт',
        'type': 'sub-head',
        'subcategory': subcategory,
        'product': Product.objects.filter(subcategory__in=subcategory)
    }
    return render(request, 'shop/shop.html', content)


def product_detail_page(request, pk):
    content = {
        'pagename': 'О товаре',
        'type': 'sub-head',
        'product': Product.objects.get(id=pk)
    }
    return render(request, 'shop/product-details.html', content)


def product_subcat_page(request, pk):
    content = {
        'pagename': 'О товаре',
        'type': 'sub-head',
        'product': Product.objects.filter(subcategory_id=pk)
    }
    return render(request, 'shop/shop.html', content)


def filter_prod(cat_id, prop):
    prods = ProductChar.objects.filter(prod__subcategory__category_id=cat_id)

    for i in prop.keys():
        prods = prods.filter(prodval__value__contains=prop[i]).distinct()

    return prods
