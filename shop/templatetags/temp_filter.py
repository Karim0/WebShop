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
    output = set()
    for x in value:
        output.add(x)
    return output


@register.filter()
def multiplication(value):
    return value * 10
