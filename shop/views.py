from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Max, Min, Avg
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery

from .models import *


def home_page(request):
    content = {
        'pagename': 'Главная страница',
        'type': '',
        'categs': Category.objects.all(),
        'prod_recom': Product.objects.annotate(prodreate=Avg('productcomment__rate')).order_by('-prodreate'),
        'questions': Question.objects.all()
    }
    return render(request, 'shop/index.html', content)


def cart_page(request):
    content = {
        'pagename': 'Корзина',
        'categs': Category.objects.all(),
        'type': 'sub-head'
    }
    return render(request, 'shop/card-page.html', content)


def about_page(request):
    content = {
        'pagename': 'О компании',
        'categs': Category.objects.all(),
        'type': 'sub-head'
    }
    return render(request, 'shop/about.html', content)


def product_detail_page(request, pk):
    product = Product.objects.get(id=pk)
    prop = set()
    prop_val = {}

    for i in Property.objects.filter(prodval__prod_char__in=product.productchar_set.all()).distinct().values_list():
        prop.add(i[1])
        prop_val[i[1]] = []
        for j in ProdVal.objects.filter(prod_char__in=product.productchar_set.all()).filter(prop=i[0]).distinct():
            prop_val[i[1]].append(j.value)

    content = {
        'categs': Category.objects.all(),
        'pagename': 'О товаре',
        'type': 'sub-head',
        'product': product,
        'prop': prop,
        'prop_val': prop_val,
    }
    return render(request, 'shop/product-details.html', content)


def product_page(request, pk):
    search = request.GET.get('search', None)
    order = request.GET.get('order', 'По рейтингу')
    subcategory = Subcategory.objects.filter(category_id=pk)
    if search:
        products = Product.objects.annotate(
            rank=SearchRank(SearchVector('name', 'desc_short', 'desc'), SearchQuery(search))).filter(
            rank__gte=0.05).order_by('-rank')
    else:
        products = Product.objects.filter(subcategory__in=subcategory)

    max_min_min = ProductChar.objects.filter(prod__in=products).aggregate(Max('price'), Min('price'))
    props = Property.objects.filter(prodval__prod_char__prod__in=products).distinct()

    max_price = int(request.GET.get('max_price', -1))
    min_price = int(request.GET.get('min_price', -1))

    for i in request.GET.keys():
        if request.GET[i] != '-1' and i not in ['max_price', 'min_price', 'search', 'order']:
            products = products.filter(productchar__prodval__value=request.GET[i]).distinct()

    if min_price != -1 and max_price != -1:
        products = products.filter(productchar__price__gte=min_price).filter(
            productchar__price__lte=max_price).distinct()

    if order == 'По рейтингу' and search:
        products = products.order_by('-rank')
    elif order == 'По рейтингу':
        products = products.annotate(rate=Avg('productcomment__rate')).order_by('-rate')
    elif order == 'Цена по возрастанию':
        products = products.annotate(price=Min('productchar__price')).order_by('price')
    elif order == 'Цена по убыванию':
        products = products.annotate(price=Min('productchar__price')).order_by('-price')

    content = {
        'pagename': 'Продукт',
        'type': 'sub-head',
        'categs': Category.objects.all(),
        'subcategory': subcategory,
        'product': products,
        'props': props,
        'max_price': max_min_min['price__max'],
        'min_price': max_min_min['price__min'],
        'max_price_curr': max_price,
        'min_price_curr': min_price,
        'search': search
    }
    return render(request, 'shop/shop.html', content)


def product_subcat_page(request, pk):
    search = request.GET.get('search', None)
    order = request.GET.get('order', None)
    if search:
        # products = Product.objects.annotate(search=SearchVector('name', 'desc_short', 'desc')).filter(search=search)
        products = Product.objects.annotate(
            rank=SearchRank(SearchVector('name', 'desc_short', 'desc'), SearchQuery(search))).filter(rank__gte=0.05)
    else:
        products = Product.objects.filter(subcategory_id=pk)

    max_min_min = ProductChar.objects.filter(prod__in=products).aggregate(Max('price'), Min('price'))
    props = Property.objects.filter(prodval__prod_char__prod__in=products).distinct()

    max_price = int(request.GET.get('max_price', -1))
    min_price = int(request.GET.get('min_price', -1))

    for i in request.GET.keys():
        if request.GET[i] != '-1' and i not in ['max_price', 'min_price', 'search', 'order']:
            products = products.filter(productchar__prodval__value=request.GET[i]).distinct()

    if min_price != -1 and max_price != -1:
        products = products.filter(productchar__price__gte=min_price).filter(
            productchar__price__lte=max_price).distinct()

    if order == 'По рейтингу' and search:
        products = products.order_by('-rank')
    elif order == 'По рейтингу':
        products = products.annotate(rate=Avg('productcomment__rate')).order_by('-rate')
    elif order == 'Цена по возрастанию':
        products = products.annotate(price=Min('productchar__price')).order_by('price')
        print(products)
    elif order == 'Цена по убыванию':
        products = products.annotate(price=Min('productchar__price')).order_by('-price')

    content = {
        'categs': Category.objects.all(),
        'pagename': 'Продукт',
        'type': 'sub-head',
        'product': products,
        'props': props,
        'max_price': max_min_min['price__max'],
        'min_price': max_min_min['price__min'],
        'max_price_curr': max_price,
        'min_price_curr': min_price,
        'search': search,
        'order': order
    }
    return render(request, 'shop/shop.html', content)


def filter_prod(cat_id, prop):
    prods = ProductChar.objects.filter(prod__subcategory__category_id=cat_id)

    for i in prop.keys():
        prods = prods.filter(prodval__value__contains=prop[i]).distinct()

    return prods
