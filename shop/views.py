from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Max, Min, Avg
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.http import response, JsonResponse
import json
from django.core.paginator import Paginator

from .models import *


def home_page(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    content = {
        'pagename': 'Главная страница',
        'categs': Category.objects.all(),
        'prod_recom': Product.objects.annotate(prodreate=Avg('productcomment__rate')).order_by('-prodreate'),
        'questions': Question.objects.all()
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

    content = {
        'pagename': 'О компании',
        'categs': Category.objects.all(),
        'type': 'sub-head'
    }
    return render(request, 'shop/about.html', content)


def product_detail_page(request, pk):
    product = Product.objects.get(id=pk)
    page = request.GET.get('page', 1)

    content = {
        'categs': Category.objects.all(),
        'pagename': 'О товаре',
        'type': 'sub-head',
        'product': product,
        'comment': Paginator(product.productcomment_set.all(), 5).get_page(page),
    }
    return render(request, 'shop/product-details.html', content)


def product_page(request, pk):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

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

    subcat = int(request.GET.get('subcat', -1))

    if subcat != -1:
        products = Product.objects.filter(subcategory_id=subcat)

    for i in request.GET.keys():
        if request.GET[i] != '-1' and i not in ['max_price', 'min_price', 'search', 'order', 'subcat', 'page']:
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

    page = request.GET.get('page', 1)
    content = {
        'pagename': 'Продукт',
        'type': 'sub-head',
        'categs': Category.objects.all(),
        'subcategory': subcategory,
        'product': Paginator(products, 9).get_page(page),
        'props': props,
        'max_price': max_min_min['price__max'],
        'min_price': max_min_min['price__min'],
        'max_price_curr': max_price,
        'min_price_curr': min_price,
        'search': search,
        'cur_subcat': subcat
    }
    return render(request, 'shop/shop.html', content)


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

    totals = 0
    for cp in cart.cartproduct_set.all():
        totals += cp.amount * cp.product.price

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
            "totals": totals,
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
    print(prod.amount)

    prod.amount = request.GET.get('amount')
    prod.save()

    print(prod.amount)
    return JsonResponse(json.dumps([]), safe=False)


def add_comment(request):
    pk = int(request.POST.get('prod_id'))
    comment = ProductComment()
    comment.prod_id = pk
    comment.rate = int(request.POST.get('rating', 0))
    comment.text = request.POST.get('text')
    comment.pub_date = datetime.datetime.now()
    comment.user_name = request.POST.get('user_name')
    comment.save()
    return redirect('shop:product_detail', pk=pk)
