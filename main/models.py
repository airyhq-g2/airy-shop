from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    birth_date = models.DateField(null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=250)
    desc = models.TextField(max_length=5000)
    price = models.FloatField(default=0)
    amount = models.IntegerField(default=0)
    pic = models.ImageField(upload_to="imgs/", max_length=500, default="../static/imgs/empty.png")
    brand = models.CharField(max_length=250, default='')

    def get_absolute_url(self):
        return reverse('main:product_detail', self.pk)

    def __str__(self):
        return '{0}-{1}'.format(self.brand, self.name)

class Transaction(models.Model):
    user = models.ForeignKey(User)
    shipping = models.CharField(max_length=250)
    status = models.CharField(max_length=250)

    def get_sum_price(self):
        price = 0
        shipping_price = 0
        orders = Order.objects.filter(transaction=self.pk)

        if(self.shipping == 'GRAB_BIKE'): shipping_price = 100
        elif(self.shipping == 'LINE_MAN'): shipping_price = 150
        elif(self.shipping == 'KERRY'): shipping_price = 200

        for order in orders: price += order.get_total_price()

        return price + shipping_price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def get_total_price(self):
        return self.product.price * self.amount

class Manager(models.Transaction):
    class Meta:
        proxy = True
        verbose_name = 'transaction'
        verbose_name_plural = 'transaction'