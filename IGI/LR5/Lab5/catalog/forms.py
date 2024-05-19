from django import forms
from .models import Order, Review
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


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Choices from 1 to 5

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ['rating', 'text']