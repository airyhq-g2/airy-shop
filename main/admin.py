from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

from .models import UserInfo, Product, Order, Transaction , Manager

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
    date_hierachy = 'created'

