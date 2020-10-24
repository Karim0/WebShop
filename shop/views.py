from django.shortcuts import render, redirect
from django.db.models import Max, Min, Avg
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
import requests as RQ

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
        'cart': cart,
        'articles': Article.objects.all()
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
        'items': cart.cartproduct_set.all().order_by('pk'),
        'cartSize': len(cart.cartproduct_set.all()),
        'tot': totals,
        'type': 'sub-head',
        'articles': Article.objects.all()

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

    items = []

    c = 0
    for i in AboutItem.objects.all():
        if c % 2 == 0:
            items.append(f'<div class="row mt-5"> \
                                <div class="col-lg-6 col-md-6"> \
                                    <img src="{i.img.url}" alt="" class="img-fluid">\
                                </div>\
                                <div class="col-lg-6 col-md-6">\
                                    <p>{i.text}</p>\
                                </div>\
                            </div>')
        else:
            items.append(f'<div class="row d-flex flex-wrap-reverse mt-5">\
                                <div class="col-lg-6 col-md-6">\
                                    <p>{i.text}</p>\
                                </div>\
                                <div class="col-lg-6 col-md-6">\
                                    <img src="{i.img.url}" alt="" class="img-fluid">\
                                </div>\
                            </div>')

        c += 1

    content = {
        'pagename': 'О компании',
        'categs': Category.objects.all(),
        'cartSize': len(cart.cartproduct_set.all()),
        'type': 'sub-head',
        'articles': Article.objects.all(),
        'items': items,

    }
    return render(request, 'shop/about.html', content)


def product_detail_page(request, pk):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    product = Product.objects.get(id=pk)
    page = request.GET.get('page', 1)

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
        'comment': Paginator(product.productcomment_set.all(), 5).get_page(page),
        'articles': Article.objects.all()

    }
    return render(request, 'shop/product-details.html', content)


def product_page(request, pk):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    category = Category.objects.get(pk=pk)
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
        'cartSize': len(cart.cartproduct_set.all()),
        'category': category,
        'max_price_curr': max_price,
        'min_price_curr': min_price,
        'search': search,
        'cur_subcat': subcat,
        'articles': Article.objects.all()

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

    return redirect('shop:product', pk=prod.prod.subcategory.category.id)


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

    for i in cart.cartproduct_set.all().order_by('pk'):
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

    for i in cart.cartproduct_set.all().order_by('pk'):
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
    cart = Cart.objects.get(session_key=request.session.session_key)

    order = Order(name=request.POST.get('full_name', 'unknown'),
                  phone=request.POST.get('phone', 'unknown'),
                  email=request.POST.get('email', 'unknown'),
                  address=f"{request.POST.get('city', 'unknown')}, {request.POST.get('address', 'unknown')}",
                  del_type=request.POST.get('delivery', 'unknown'),
                  pay_type=request.POST.get('payment', 'unknown'),
                  total_sum=0)
    order.save()
    tot_sum = 0
    for i in cart.cartproduct_set.all():
        tot_sum += i.product.price * i.amount
        i.product.sold += 1
        i.product.save()

        position = OrderPosition(order=order,
                                 product=i.product,
                                 amount=i.amount)
        position.save()

    order.total_sum = tot_sum
    order.save()
    cart.delete()

    if order.pay_type == 'картой':
        login = "test_merch"
        password = "A12345678a"

        auth_data = {'login': login,
                     'password': password}

        auth_url = "https://api.yii2-stage.test.wooppay.com/v1/auth"

        auth_data = RQ.request("POST", auth_url, data=auth_data).json()

        order_url = "https://api.yii2-stage.test.wooppay.com/v1/invoice/create"

        order_data = {
            "reference_id": 72234 * order.id,
            "amount": tot_sum,
            "service_name": "test_merch_invoice",
            "merchant_name": 384310,
            "option": 0,
            "card_forbidden": 0,
            "requestUrl": "http://213.211.91.155:8000/shop/product/order_confirmation?order_id=" + str(order.id)
        }

        headers = {
            'Authorization': auth_data['token'].replace('jwt ', 'Bearer ')
        }

        response = RQ.request("POST", order_url, headers=headers, data=order_data).json()

        return redirect(response['operation_url'])

    return redirect('shop:index')


def confirmation(request):
    print('successful')
    order = Order.objects.get(request.GET['order_id'])
    order.checked = "оплачен"
    order.save()

    return redirect('shop:index')


def add_comment(request):
    pk = int(request.POST.get('prod_id'))
    comment = ProductComment()
    comment.prod_id = pk
    comment.rate = int(request.POST.get('rating', 0))
    comment.text = request.POST.get('text')
    comment.pub_date = datetime.datetime.now()
    comment.phone_number = request.POST.get('phone_number')
    comment.user_name = request.POST.get('user_name')
    comment.save()
    return redirect('shop:product_detail', pk=pk)


def callback(request):

    print(request.GET['name'])
    call = Calling(full_name=request.GET['name'],
                   phone=request.GET['phone'])
    call.save()
    return JsonResponse(json.dumps({}), safe=False)
