from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    birth_date = models.DateField(null=True, blank=True)

class Product(models.Model):
    name = models.TextField(max_length=1000,null=False)
    desc = models.TextField(max_length=1000)
    price = models.FloatField()
    amount = models.IntegerField()
    pic = models.ImageField(upload_to="imgs/", default="static/imgs/product_thumbnail.jpg")

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
