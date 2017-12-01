from django.contrib.auth import login, authenticate, views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm, OrderForm, UserEditForm, UploadPayInForm
from .models import Product, Order, Transaction, UserInfo
from django.contrib.auth.models import User

def get_cart_context(user):
    if not user.is_authenticated: return {}
    transaction = Transaction.objects.get(user=user, status='active')
    orders = transaction.order_set.all()
    grand_total_price = transaction.get_grand_total_price()
    sub_total_price = transaction.get_sub_total_price()
    return {
        'orders': orders,
        'sub_total_price': sub_total_price,
        'grand_total_price': grand_total_price,
        'transaction': transaction,
    }

def indexView(request):
    return render(request, 'main/index.html')


class CatalogueView(ListView):
    template_name = 'main/catalogue.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(CatalogueView, self).get_context_data(**kwargs)
        context.update(get_cart_context(self.request.user))
        return context

    def get_queryset(self):
        result = super(CatalogueView, self).get_queryset()
        # priceBox = self.request.GET.get('price')
        # brandBox = self.request.GET.get('brand')
        # nameBox = self.request.GET.get('name')
        query = self.request.GET.get('q')
        if query:
            try:
                  data = self.request.GET.get("choice")
                  if data == "price":
                    result = Product.objects.filter(price__lte=query)
                  if data == "brand":
                    result = Product.objects.filter(brand__icontains=query)
                  if data == "name":
                    result = Product.objects.filter(name__icontains=query)
            except ObjectDoesNotExist:
                return []
        return result


class ProductDetailView(DetailView):
    template_name = 'main/product-detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context.update(get_cart_context(self.request.user))
        return context


class LoginView(views.LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True
    redirect_field_name = reverse_lazy('main:catalogue')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update(get_cart_context(self.request.user))
        return context


def registerView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Transaction.objects.create(
                user=user,
                status='active'
            ).save()
            UserInfo.objects.create(user=user).save()
            return redirect('/catalogue')
    else:
        form = SignUpForm()

    return render(request, 'main/register.html', {'form': form})


class CartView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('main:login')
    template_name = 'main/cart.html'
    model = Order

    def get_queryset(self):
        transaction = Transaction.objects.get(user=self.request.user, status='active')
        return transaction.order_set.all()

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context.update(get_cart_context(self.request.user))
        return context


@login_required
def addToCart(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            pk = form.cleaned_data.get('product')
            try:
                transaction = Transaction.objects.get(
                    user=request.user,
                    status='active',
                )
            except ObjectDoesNotExist:
                transaction = Transaction.objects.create(
                    user=request.user,
                    status="active"
                )
            transaction.save()
            order = Order.objects.create(
                user=request.user,
                product=Product.objects.get(pk=pk),
                amount=amount,
                transaction=transaction
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


class PaymentSlipView(LoginRequiredMixin, ListView):
    template_name = 'main/payment-slip.html'
    model = Order
    login_url = reverse_lazy('main:login')

    def get(self, request, *args, **kwargs):
        user_info = UserInfo.objects.get(user=request.user)
        first_name = request.user.first_name
        last_name = request.user.last_name
        address = user_info.address
        if first_name != '' and last_name != '' and address != '':
            return super(PaymentSlipView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('main:profile_edit_info'))

    def get_queryset(self):
        self.transaction = Transaction.objects.get(pk=self.kwargs['pk'])
        return Order.objects.filter(transaction=self.transaction)

    def get_context_data(self, **kwargs):
        context = super(PaymentSlipView, self).get_context_data(**kwargs)
        context.update({
            'transaction': self.transaction,
            'user_info': UserInfo.objects.get(user=self.request.user)
        })
        return context


class ProfileDashBoardView(LoginRequiredMixin, DetailView):
    template_name = 'profile/dashboard.html'
    model = UserInfo
    login_url = reverse_lazy('main:login')

    def get_object(self, queryset=None):
        return UserInfo.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProfileDashBoardView, self).get_context_data(**kwargs)
        context.update(get_cart_context(self.request.user))
        return context


class ProfileTrackingView(LoginRequiredMixin, ListView):
    template_name = 'profile/tracking.html'
    model = Transaction
    login_url = reverse_lazy('main:login')


    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileTrackingView, self).get_context_data(**kwargs)
        context.update(get_cart_context(self.request.user))
        return context


class ProfileEditInfo(LoginRequiredMixin, FormView):
    template_name = 'profile/edit-info.html'
    form_class = UserEditForm
    success_url = reverse_lazy('main:profile_dashboard')
    login_url = reverse_lazy('main:login')

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        user_info = UserInfo.objects.get(user=self.request.user)

        user_name = form.cleaned_data.get('user_name')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        birth_date = form.cleaned_data.get('birth_date')
        address = form.cleaned_data.get('address')

        if user_name != '': user.username = user_name
        if email != '': user.email = email
        if first_name != '': user.first_name = first_name
        if last_name != '': user.last_name = last_name
        if birth_date != '': user_info.birth_date = birth_date
        if address != '': user_info.address = address

        user.save()
        user_info.save()

        return super(ProfileEditInfo, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileEditInfo, self).get_context_data(**kwargs)
        context.update(get_cart_context(self.request.user))
        return context


class ProfileUploadPayInView(LoginRequiredMixin, FormView):
    template_name = 'profile/upload-pay-in.html'
    success_url = reverse_lazy('main:profile_dashboard')
    login_url = reverse_lazy('main:login')
    form_class = UploadPayInForm

    def get_context_data(self, **kwargs):
        context = super(ProfileUploadPayInView, self).get_context_data(**kwargs)
        context.update(get_cart_context(self.request.user))
        return context

    def form_valid(self, form):
        transaction = Transaction.objects.get(user=self.request.user, status='active')
        transaction.slip = form.cleaned_data.get('slip')
        transaction.save()
        return super(ProfileUploadPayInView, self).form_valid(form)

def contactView(request):
    return render(request, 'main/contact.html')
#test