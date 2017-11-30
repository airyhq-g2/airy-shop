from django.contrib.auth import login, authenticate, views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm, OrderForm
from .models import Product, Order, Transaction


def indexView(request):
    return render(request, 'main/index.html')


class CatalogueView(ListView):
    template_name = 'main/catalogue.html'
    model = Product
    additional_context = {}

    def get_context_data(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            orders = Order.objects.filter(user=self.request.user)
            sub_total_price = 0
            try:
                transaction = orders.first().transaction
                sub_total_price = transaction.get_grand_total_price()
            except AttributeError as error:
                sub_total_price = 0
            self.additional_context = {
                'cart': orders,
                'sub_total_price': sub_total_price
            }
        context = super(CatalogueView, self).get_context_data(**kwargs)
        context.update(self.additional_context)
        return context

    def get_queryset(self):
        result = super(CatalogueView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            try:
                result = [Product.objects.filter(product__brand__icontains=query)]
            except ObjectDoesNotExist:
                return []
        return result


class ProductDetailView(DetailView):
    template_name = 'main/product-detail.html'
    model = Product

    additional_context = {}

    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            orders = Order.objects.filter(user=self.request.user)
            sub_total_price = 0
            try:
                transaction = orders.first().transaction
                sub_total_price = transaction.get_grand_total_price()
            except AttributeError as error:
                sub_total_price = 0
            self.additional_context = {
                'cart': orders,
                'sub_total_price': sub_total_price
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
        transaction = Transaction.objects.get_or_create(user=self.request.user, shipping='KERRY', status='active')[0]
        return Order.objects.filter(transaction=transaction)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user)
        transaction = orders.first().transaction
        context.update({
            'cart': orders,
            'sub_total_price': transaction.get_sub_total_price(),
            'grand_total_price': transaction.get_grand_total_price(),
            'transaction': transaction.pk
        })
        return context


@login_required
def addToCart(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            pk = form.cleaned_data.get('product')
            shipping = 'KERRY'
            transaction = Transaction.objects.get_or_create(
                user=request.user,
                status='active',
                shipping=shipping
            )
            order = Order.objects.create(
                user=request.user,
                product=Product.objects.get(pk=pk),
                amount=amount,
                transaction=transaction[0]
            )
            order.save()
    return HttpResponseRedirect(reverse_lazy('main:catalogue'))


@login_required
def removeFromCart(request):
    if request.method == 'POST':
        pk = request.POST.get('order')
        order = Order.objects.get(pk=pk)
        order.delete()
        return HttpResponseRedirect(reverse_lazy('main:cart'))


def update_order_ajax(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse_lazy('main:cart'))
    amount = request.POST.get('amount')
    pk = request.POST.get('order')
    try:
        order = Order.objects.get(pk=pk)
        order.amount = int(amount)
        order.save()
        total_price = order.get_total_price()
        sub_total_price = order.transaction.get_sub_total_price()
        grand_total_price = order.transaction.get_grand_total_price()
        return JsonResponse({
            'amount': order.amount,
            'productId': order.product_id,
            'totalPrice': total_price,
            'subTotalPrice': sub_total_price,
            'grandTotalPrice': grand_total_price
        })
    except ObjectDoesNotExist as error:
        return JsonResponse({'err': error.__str__()})



def change_shipping(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse_lazy('main:cart'))
    transaction_pk = request.POST.get('transaction')
    shipping = request.POST.get('shipping')
    try:
        transaction = Transaction.objects.get(pk=transaction_pk)
        transaction.shipping = shipping
        transaction.save()
        grand_total_price = transaction.get_grand_total_price()
        return JsonResponse({
            'grandTotalPrice': grand_total_price,
            'shipping': shipping
        })
    except ObjectDoesNotExist as error:
        return JsonResponse({'err': error.__str__()})


class PaymentSlipView(ListView):
    template_name = 'main/paymeny-slip.html'
    model = Order

    def get_queryset(self):
        self.transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        return Order.objects.filter(transaction=self.transaction)

    def get_context_data(self, **kwargs):
        context = super(PaymentSlipView, self).get_context_data(**kwargs)
        context.update({'transaction': self.transaction})
        return context
