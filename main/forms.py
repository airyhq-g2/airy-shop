from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderForm(forms.Form):
    amount = forms.IntegerField()
    product = forms.IntegerField()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
