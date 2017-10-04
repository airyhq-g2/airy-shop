from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from main import views

app_name = 'main'

urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^catalogue/$', views.catalogueView, name='catalogue'),
    url('^products/$', views.detailView, name='product_detail'),
    url('^login/$', views.LoginView.as_view(), name='login'),
    url('^logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('main:catalogue')), name='logout'),
    url('^register/$', views.registerView, name='register'),
    url('^cart/$', views.cartView, name='cart'),
]