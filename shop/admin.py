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

class ElementInline(admin.TabularInline):
    model = OrderPosition
    extra = 0
    fields = ['product', 'amount']

class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order
        fields = '__all__'

    list_display = ('name', 'address', 'email', 'phone', 'del_type', 'pay_type', 'total_sum', 'pub_date', 'checked')
    list_filter = ('checked', 'del_type', 'pay_type')
    inlines = (ElementInline,)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductChar)
admin.site.register(ProdVal)
admin.site.register(Property)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(ProductComment)
admin.site.register(Calling)
admin.site.register(Question)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(AboutItem)
admin.site.register(SiteProfile)




