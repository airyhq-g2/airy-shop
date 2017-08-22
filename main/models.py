from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
# Create your models here.

class Product(models.Model):
    name = models.TextField(max_length=1000,null=False)
    desc = models.TextField(max_length=1000)
    price = models.FloatField()
    amount = models.IntegerField()
    pic = models.ImageField(upload_to="media/", default="static/imgs/product_thumbnail.jpg")

class Order(models.Model):
    user = models.ForeignKey(Profile)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    date = models.DateTimeField()
    status = models.IntegerField()
