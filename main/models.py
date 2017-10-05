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

    def get_absolute_url(self):
        return reverse('main:product_detail', self.pk)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    status = models.IntegerField()

    def get_total_price(self):
        return self.product.price * self.amount
