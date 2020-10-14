from shop.models import *


# cat_id - cateroty id
# prop - dict
# prop = {'color': 'black'}
#
def filter_prod(cat_id, prop):
    prods = ProductChar.objects.filter(prod__subcategory__category_id=cat_id)

    for i in prop.keys():
        prods = prods.filter(prodval__value__contains=prop[i]).distinct()

    return prods
