from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Max, Min, Avg
from django.http import response, JsonResponse
import json

from .models import *


def home_page(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    content = {
        'pagename': 'Главная страница',
        'categs': Category.objects.all(),
        'prod_recom': Product.objects.annotate(prodreate=Avg('productcomment__rate')).order_by('-prodreate'),
        'questions': Question.objects.all(),
        'cartSize': len(cart.cartproduct_set.all()),
        'cart': cart

    }
    return render(request, 'shop/index.html', content)


def cart_page(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    totals = 0

    for cp in cart.cartproduct_set.all():
        totals += cp.amount * cp.product.price

    content = {
        'pagename': 'Корзина',
        'categs': Category.objects.all(),
        'items': cart.cartproduct_set.all(),
        'cartSize': len(cart.cartproduct_set.all()),
        'tot': totals
    }
    return render(request, 'shop/card-page.html', content)


def about_page(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    content = {
        'pagename': 'О компании',
        'categs': Category.objects.all(),
        'cartSize': len(cart.cartproduct_set.all()),
        'type': 'sub-head'
    }
    return render(request, 'shop/about.html', content)


def product_page(request, pk):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    subcategory = Subcategory.objects.filter(category_id=pk)
    products = Product.objects.filter(subcategory__in=subcategory)
    max_min_min = ProductChar.objects.filter(prod__in=products).aggregate(Max('price'), Min('price'))
    props = Property.objects.filter(prodval__prod_char__prod__in=products).distinct()

    max_price = int(request.GET.get('max_price', -1))
    min_price = int(request.GET.get('min_price', -1))

    for i in request.GET.keys():
        if request.GET[i] != '-1' and i not in ['max_price', 'min_price']:
            products = products.filter(productchar__prodval__value=request.GET[i]).distinct()

    if min_price != -1 and max_price != -1:
        products = products.filter(productchar__price__gte=min_price).filter(
            productchar__price__lte=max_price).distinct()
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
        'cartSize': len(cart.cartproduct_set.all()),

    }
    return render(request, 'shop/shop.html', content)


def product_detail_page(request, pk):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    product = Product.objects.get(id=pk)

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    content = {
        'categs': Category.objects.all(),
        'pagename': 'О товаре',
        'type': 'sub-head',
        'cartSize': len(cart.cartproduct_set.all()),
        'product': product,
        'prodch': product.productchar_set.all(),
    }
    return render(request, 'shop/product-details.html', content)


def product_subcat_page(request, pk):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    products = Product.objects.filter(subcategory_id=pk)
    max_min_min = ProductChar.objects.filter(prod__in=products).aggregate(Max('price'), Min('price'))
    props = Property.objects.filter(prodval__prod_char__prod__in=products).distinct()

    max_price = int(request.GET.get('max_price', -1))
    min_price = int(request.GET.get('min_price', -1))

    for i in request.GET.keys():
        if request.GET[i] != '-1' and i not in ['max_price', 'min_price']:
            products = products.filter(productchar__prodval__value=request.GET[i]).distinct()

    if min_price != -1 and max_price != -1:
        products = products.filter(productchar__price__gte=min_price).filter(
            productchar__price__lte=max_price).distinct()
    content = {
        'categs': Category.objects.all(),
        'pagename': 'Продукт',
        'type': 'sub-head',
        'product': products,
        'props': props,
        'max_price': max_min_min['price__max'],
        'min_price': max_min_min['price__min'],
        'cartSize': len(cart.cartproduct_set.all()),

        'max_price_curr': max_price,
        'min_price_curr': min_price,
    }
    return render(request, 'shop/shop.html', content)


def filter_prod(cat_id, prop):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    prods = ProductChar.objects.filter(prod__subcategory__category_id=cat_id)

    for i in prop.keys():
        prods = prods.filter(prodval__value__contains=prop[i]).distinct()

    return prods


def addCart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    id = request.POST['prodchars']
    amount = request.POST['amount']
    prod = ProductChar.objects.get(pk=id)
    pass_bool = True

    for i in cart.cartproduct_set.all():
        if prod == i.product:
            pass_bool = False
            i.amount += int(amount)
            i.save()

    if pass_bool:
        cartElement = CartProduct(cart=cart, product=prod, amount=amount)
        cartElement.save()

    return redirect('shop:cart')


def delete_item(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    prod = cart.cartproduct_set.get(id=request.GET.get('product_id'))

    prod.delete()

    cartList = []

    for i in cart.cartproduct_set.all():
        props = []
        for j in i.product.prodval_set.all():
            props.append({
                'prop': j.prop.name,
                'value': j.value
            })
        img = i.product.prod.productphoto_set.all().first()
        cartList.append({
            "name": i.product.prod.name,
            "price": i.product.price,
            "img": img.img.url,
            "props": props,
            "alt": img.alt,
            "id": i.id,
            "amount": i.amount
        })

    return JsonResponse(json.dumps(cartList), safe=False)


def changeAmount(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    prod = cart.cartproduct_set.get(id=request.GET.get('product_id'))

    if int(request.GET.get('amount')) <= 0:
        prod.delete()
    else:
        prod.amount = int(request.GET.get('amount'))
        prod.save()
    cartList = []

    for i in cart.cartproduct_set.all():
        props = []
        for j in i.product.prodval_set.all():
            props.append({
                'prop': j.prop.name,
                'value': j.value
            })
        img = i.product.prod.productphoto_set.all().first()
        cartList.append({
            "name": i.product.prod.name,
            "price": i.product.price,
            "img": img.img.url,
            "props": props,
            "alt": img.alt,
            "id": i.id,
            "amount": i.amount
        })
    return JsonResponse(json.dumps(cartList), safe=False)


def make_order(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    if request.method == 'POST':
        print(request.POST.get('full_name'))

