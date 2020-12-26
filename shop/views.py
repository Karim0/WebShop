from django.shortcuts import render, redirect
from django.db.models import Max, Min, Avg, Sum
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
        'pagename': f'{SiteProfile.objects.first().page_name} | Главная страница',
        'categs': Category.objects.all(),
        'prod_recom': Product.objects.annotate(prodreate=Avg('productcomment__rate')).order_by('-prodreate')[:10],
        'questions': Question.objects.all(),
        'cartSize': len(cart.cartproduct_set.all()),
        'cart': cart,
        'articles': Article.objects.all(),
        'site': SiteProfile.objects.first()
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
        'articles': Article.objects.all(),
        'questions': Question.objects.all(),
        'site': SiteProfile.objects.first()

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
        'pagename': 'О магазине',
        'categs': Category.objects.all(),
        'cartSize': len(cart.cartproduct_set.all()),
        'type': 'sub-head',
        'articles': Article.objects.all(),
        'items': items,
        'questions': Question.objects.all(),
        'site': SiteProfile.objects.first()

    }
    return render(request, 'shop/about.html', content)


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
        'pagename': f'О товаре | {product.name}',
        'type': 'sub-head',
        'cartSize': len(cart.cartproduct_set.all()),
        'product': product,
        'pr': product.productchar_set.all()[0],
        'comment': product.productcomment_set.all(),
        'articles': Article.objects.all(),
        'questions': Question.objects.all(),

        'site': SiteProfile.objects.first()

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
    order = request.GET.get('sortby')

    if (order != 'popularity') and (order != 'price_asc') and (order != 'price_desc'):
        order = 'popularity'

    subcategory = Subcategory.objects.filter(category_id=pk)

    products = Product.objects.filter(subcategory__in=subcategory)

    max_min_min = ProductChar.objects.filter(prod__in=products).aggregate(Max('price'), Min('price'))

    props = {}

    for p in Property.objects.filter(prodval__prod_char__prod__in=products).distinct():
        props[p.id] = [p, 'Не выбрано', ]

    max_price = int(request.GET.get('max_price', -1))
    min_price = int(request.GET.get('min_price', -1))

    subcat = int(request.GET.get('subcat', -1))

    if subcat != -1:
        products = Product.objects.filter(subcategory_id=subcat)
    else:
        subcat = int(request.GET.get('cur_subcat', -1))
        if subcat != -1:
            products = Product.objects.filter(subcategory_id=subcat)

    for i in request.GET.keys():
        if request.GET[i] != '-1' and i not in ['max_price', 'min_price', 'search', 'order', 'subcat', 'page',
                                                'sortby', 'cur_subcat']:
            if request.GET[i]:
                val = request.GET[i].split('_')[1]
                products = products.filter(productchar__prodval__value=request.GET[i].split('_')[2]).distinct()
                p_id = ProdVal.objects.get(id=val).prop.id
                p_val = ProdVal.objects.get(id=val).value
                props[p_id][1] = p_val

    if min_price != -1 and max_price != -1:
        products = products.filter(productchar__price__gte=min_price).filter(
            productchar__price__lte=max_price).distinct()

    if order == 'popularity':
        order = 'Популярности'
        products = products.annotate(rate=Sum('productcomment__rate')).order_by('-rate')
    elif order == 'price_asc':
        order = 'Цена по возрастанию'
        products = products.annotate(price=Min('productchar__price')).order_by('price')
    elif order == 'price_desc':
        order = 'Цена по убыванию'
        products = products.annotate(price=Min('productchar__price')).order_by('-price')

    page = request.GET.get('page', 1)

    if search:
        products = Product.objects.filter(name__contains=search[1:].strip().lower())

    content = {
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
        'articles': Article.objects.all(),
        'questions': Question.objects.all(),
        'site': SiteProfile.objects.first(),
        'cur_sort': order,
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

    id = int(request.POST['prodchars'])
    amount = request.POST['amount']
    isFast = request.POST['fast']
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

    if isFast == 'fast':
        data = {'amount': len(cart.cartproduct_set.all())}
        return JsonResponse(json.dumps(data), safe=False)
    else:
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
                                 product=i.product.__str__(),
                                 amount=i.amount)
        position.save()

    order.total_sum = tot_sum

    if order.pay_type == 'картой':
        login = SiteProfile.objects.first().paylogin
        password = SiteProfile.objects.first().paypassword

        auth_data = {'login': login,
                     'password': password}

        auth_url = "https://api.yii2-stage.test.wooppay.com/v1/auth"

        auth_data = RQ.request("POST", auth_url, data=auth_data).json()

        print(login, password)
        print(auth_data)

        order_url = "https://api.yii2-stage.test.wooppay.com/v1/invoice/create"

        order_data = {
            "reference_id": 'hanok-market-payment' + str(order.id),
            "amount": tot_sum,
            "option": 0,
            "card_forbidden": 0,
            "requestUrl": "http://hanok-market.kz/shop/product/order_confirmation?order_id=" + str(order.id)
        }

        headers = {
            'Authorization': auth_data['token'].replace('jwt ', 'Bearer ')
        }

        response = RQ.request("POST", order_url, headers=headers, data=order_data).json()

        print(response)

        order.save()
        cart.delete()

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

    data = []
    for c in Product.objects.get(pk=pk).productcomment_set.all():
        data.append({
            'name': c.user_name,
            'text': c.text,
            'date': str(c.pub_date),
            'rate': c.rate
        })

    return JsonResponse(json.dumps(data), safe=False)


def callback(request):
    print(request.GET['name'])
    call = Calling(full_name=request.GET['name'],
                   phone=request.GET['phone'])
    call.save()
    return JsonResponse(json.dumps({}), safe=False)



def privacy(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    content = {
        'pagename': f'{SiteProfile.objects.first().page_name} | ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ',
        'categs': Category.objects.all(),
        'questions': Question.objects.all(),
        'cartSize': len(cart.cartproduct_set.all()),
        'cart': cart,
        'articles': Article.objects.all(),
        'site': SiteProfile.objects.first()
    }
    return render(request, 'shop/privacy.html', content)


def oferta(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart(session_key=session_key)
        cart.save()

    content = {
        'pagename': f'{SiteProfile.objects.first().page_name} | ПУБЛИЧНАЯ ОФЕРТА',
        'categs': Category.objects.all(),
        'questions': Question.objects.all(),
        'cartSize': len(cart.cartproduct_set.all()),
        'cart': cart,
        'articles': Article.objects.all(),
        'site': SiteProfile.objects.first()
    }
    return render(request, 'shop/oferta.html', content)


