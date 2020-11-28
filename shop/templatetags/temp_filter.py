from django import template
from django.template.defaultfilters import stringfilter

# from shop.models import CartProduct
register = template.Library()


@register.filter()
def is_contains(value, key):
    return key in value.values()


@register.filter()
def get_val_map(value, key):
    return value[key]


@register.filter()
def unique(value):
    output = []
    for x in value:
        print(x.value)
        if not check_exist(output, x.value):
            output.append(x)
    return output


def check_exist(arr, x):
    for i in arr:
        if x == i.value:
            return True
    return False


@register.filter()
def multiplication(value):
    return value * 10


@register.filter()
def pagi_cut(value, p):
    if value.find('?') >= 0:
        pattern = value.split('?')
        if pattern[1].find('page=') != -1:
            return pattern[0] + '?' + '&'.join(pattern[1].split('&')[:-1]) + '&page=' + str(p)
        else:
            return f'{pattern[0]}?{pattern[1]}&page={p}'
    else:
        return f'{value}?page={p}'
