from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

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

class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Airy Shop Admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Business Administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Airy Shop Admin')

admin_site = MyAdminSite()