from django.contrib import admin

from .models import UserInfo, Product, Order

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Product)
admin.site.register(Order)