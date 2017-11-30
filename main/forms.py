from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserInfo


class OrderForm(forms.Form):
    amount = forms.IntegerField()
    product = forms.IntegerField()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class UserEditForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100, required=False)
    first_name = forms.CharField(label='First name', max_length=100, required=False)
    last_name = forms.CharField(label='Last name', max_length=100, required=False)
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput, required=False)
    birth_date = forms.DateTimeField(label='Birth date', widget=forms.DateInput, required=False)
    address = forms.CharField(label='Address', max_length=500, widget=forms.Textarea, required=False)
