from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

from .models import UserInfo, Product, Order, Transaction, Manager

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.site_header = 'Airy Business Admin'
admin.site.site_title = 'Airy Administration'
admin.site.index_title = 'Airy Administration'


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    change_list_template = 'admin/manager.html'
    date_hierarchy = 'date'

    def changelist_view(self, request, extra_context=None):
        all_brands = {}
        count_orders = []
        count_sales = []
        for product in Product.objects.all(): all_brands[product.brand] = product.brand

        summary = []

        total_sale = 0
        for order in Order.objects.all(): total_sale += order.get_total_price()

        for brand in all_brands:
            brand_orders = Order.objects.filter(product__brand=brand)
            count_orders.append(brand_orders.count())
            total_price = 0
            for each in brand_orders: total_price += each.get_total_price()
            count_sales.append(total_price)
            summary.append([brand, brand_orders.count(), total_price, ((total_price / total_sale) * 100)])

        c = {
            'summary': summary,
            'all_brands': all_brands,
            'count_orders': count_orders,
            'count_sales': count_sales,
            'summary_sale': total_sale,
            'summary_order': len(count_orders)
        }

        response = super(ManagerAdmin, self).changelist_view(
            request,
            extra_context=c,
        )
        return response
