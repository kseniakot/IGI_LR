from django import forms
from .models import Order
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]