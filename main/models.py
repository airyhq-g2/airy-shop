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
    shipping = models.CharField(max_length=250, default='KERRY')
    status = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True)

    def get_shipping_fee(self):
        if (self.shipping == 'GRAB_BIKE'):
            return 100
        elif (self.shipping == 'LINE_MAN'):
            return 150
        elif (self.shipping == 'KERRY'):
            return 200

    def get_sub_total_price(self):
        price = 0
        orders = Order.objects.filter(transaction=self.pk)

        for order in orders: price += order.get_total_price()

        return price

    def get_grand_total_price(self):
        price = self.get_sub_total_price()
        shipping_fee = self.get_shipping_fee()
        return price + shipping_fee

    def __str__(self):
        return 'T#{0}-{1}-{2}-{3}'.format(self.pk, self.user, self.shipping, self.status)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def get_total_price(self):
        return self.product.price * self.amount

    def __str__(self):
        return 'O#{0}-{1}-{2}-{3}-{4}-{5}'.format(self.pk, self.user, self.product, self.amount, self.date,
                                                  self.transaction_id)


class Manager(Transaction):
    class Meta:
        proxy = True
        verbose_name = 'Manager'
        verbose_name_plural = 'Manager'