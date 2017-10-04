from django.contrib.auth import login, authenticate, views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from .forms import SignUpForm
from .models import Product


# Create your views here.
def indexView(request):
    return render(request, 'main/index.html')


def catalogueView(request):
    return render(request, 'main/catalogue.html')


class CatalogueView(ListView):
    template_name = 'main/catalogue.html'
    model = Product

def detailView(request):
    return render(request, 'main/product-detail.html')


class LoginView(views.LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True
    redirect_field_name = reverse_lazy('main:catalogue')


def registerView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
        return redirect('/catalogue')
    else:
        form = SignUpForm()
    return render(request, 'main/register.html', {'form': form})


def cartView(request):
    return render(request, 'main/cart.html')