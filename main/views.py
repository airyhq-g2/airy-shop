from django.contrib.auth import login, authenticate, views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm, OrderForm
from .models import Product, Order , Transaction


# Create your views here.
def indexView(request):
    return render(request, 'main/index.html')

class CatalogueView(ListView):
    template_name = 'main/catalogue.html'
    model = Product
    additional_context = {}


    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            total_price = 0
            orders = Order.objects.filter(user=self.request.user)

            for order in orders:
                total_price += order.get_total_price()

            self.additional_context = {
                'cart': orders,
                'total_price': total_price
            }
        context = super(CatalogueView, self).get_context_data(**kwargs)
        context.update(self.additional_context)
        return context



class ProductDetailView(DetailView):
    template_name = 'main/product-detail.html'
    model = Product

    additional_context = {}

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            total_price = 0
            orders = Order.objects.filter(user=self.request.user)

            for order in orders:
                total_price += order.get_total_price()

            self.additional_context = {
                'cart': orders,
                'total_price': total_price
            }
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context.update(self.additional_context)
        return context


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


class CartView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('main:login')
    template_name = 'main/cart.html'
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        total_price = 0
        orders = Order.objects.filter(user=self.request.user)

        for order in orders:
            total_price += order.get_total_price()

        context.update({
            'cart': orders,
            'total_price': total_price
        })
        return context


def addToCart(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('main:login'))
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            pk = form.cleaned_data.get('product')
            try:
                trans = Transaction.objects.get(user=request.user, status="inactive")
                order = Order.objects.create(
                        user=request.user,
                        product=Product.objects.get(pk=pk),
                        amount=amount,
                        transaction=trans
                )
                order.save()
            except ObjectDoesNotExist as error:
                trans = Transaction.objects.create(
                    user = request.user,
                    shipping = "KERRY",
                    status = "active"
                )
                trans.save()
                order = Order.objects.create(
                        user=request.user,
                        product=Product.objects.get(pk=pk),
                        amount=amount,
                        transaction=trans
                )
                order.save()
            return HttpResponseRedirect(reverse_lazy('main:catalogue'))


@login_required
def removeFromCart(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('product')
            order = Order.objects.get(pk=pk)
            order.delete()
            return HttpResponseRedirect(reverse_lazy('main:cart'))

