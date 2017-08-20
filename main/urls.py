from django.conf.urls import url
from main import views

app_name = 'main'

urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^catalogue$', views.catalogueView, name='catalogue'),
    url('^products$', views.detailView, name='product_detail'),
    url('^login$', views.loginView, name='login'),
    url('^register$', views.registerView, name='register'),
    url('^cart$', views.cartView, name='cart'),
]