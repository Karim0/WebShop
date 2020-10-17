from django.contrib import admin
from shop.models import *
from nested_admin.nested import NestedStackedInline, NestedModelAdmin, NestedTabularInline


class ProductPhotoAdmin(NestedTabularInline):
    model = ProductPhoto
    extra = 0


class ValCharAdmin(NestedTabularInline):
    model = ProdVal
    extra = 0
    fields = ['prop', 'value']
    classes = ['prod_val']


class ProdCharAdmin(NestedTabularInline):
    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
            'all': ('css/admin_panel.css',)
        }

    model = ProductChar
    inlines = [ValCharAdmin]
    extra = 0

    classes = ['prod_char']


class ProductAdmin(NestedModelAdmin):
    model = Product
    inlines = [ProdCharAdmin, ProductPhotoAdmin]


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductChar)
admin.site.register(ProdVal)
admin.site.register(Property)
admin.site.register(Category)
admin.site.register(Subcategory)
