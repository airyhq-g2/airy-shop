from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# from django.conf.urls import patterns, include
# from myproject.admin import admin_site

from main import views

app_name = 'main'

urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^catalogue/$', views.CatalogueView.as_view(), name='catalogue'),
    url('^product/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='product_detail'),
    url('^login/$', views.LoginView.as_view(), name='login'),
    url('^logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('main:catalogue')), name='logout'),
    url('^register/$', views.registerView, name='register'),
    url('^cart/$', views.CartView.as_view(), name='cart'),
    url('^add-product/$', views.addToCart, name='add_to_cart'),
    url('^remove-product/$', views.removeFromCart, name='remove_from_cart'),
    url('^update-order/$', views.update_order_ajax, name='update_order_ajax'),
    url('^change-shipping/$', views.change_shipping, name='change-shipping'),
    url('^payment-slip/(?P<pk>\d+)/$', views.PaymentSlipView.as_view(), name='payment_slip'),
    url('^profile/dashboard/$', views.ProfileDashBoardView.as_view(), name='profile_dashboard'),
    url('^profile/tracking/$', views.ProfileTrackingView.as_view(), name='profile_tracking'),
    url('^profile/edit-info/$', views.ProfileEditInfo.as_view(), name='profile_edit_info'),
    url('^contact/$', views.ContactView.as_view(), name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
