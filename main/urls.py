from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from main import views

app_name = 'main'

urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^catalogue/$', views.CatalogueView.as_view(), name='catalogue'),
    url('^product/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='product_detail'),
    url('^login/$', views.LoginView.as_view(), name='login'),
    url('^logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('main:catalogue')), name='logout'),
    url('^register/$', views.registerView, name='register'),
    url('^cart/$', views.cartView, name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
