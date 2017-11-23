from django.contrib import admin

from .models import UserInfo, Product, Order, Transaction , Manager

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Order)

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    change_list_template = 'admin/manager.html'
    date_hierachy = 'created'