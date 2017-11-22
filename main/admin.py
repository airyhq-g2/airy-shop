from django.contrib import admin

from .models import UserInfo, Product, Order, Transaction

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Order)