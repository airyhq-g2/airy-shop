from django.shortcuts import render

# Create your views here.
def indexView(request):
    return render(request, 'main/index.html')


def catalogueView(request):
    return render(request, 'main/catalogue.html')


def detailView(request):
    return render(request, 'main/product-detail.html')


def loginView(request):
    return render(request, 'main/login.html')


def registerView(request):
    return render(request, 'main/register.html')


def cartView(request):
    return render(request, 'main/cart.html')