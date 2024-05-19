from django.core.validators import RegexValidator
from .models import Order, Review
from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        help_text="Required. Format: YYYY-MM-DD",
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'max': date.today().strftime('%Y-%m-%d')})
    )
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+375 \((29|33|44|25)\) \d{3}-\d{2}-\d{2}$',
                message="Phone number must be entered in the format: '+375 (29) XXX-XX-XX'. Up to 15 digits allowed."
            )
        ]
    )

    CITIES = [
        ('Minsk', 'Minsk'),
        ('Brest', 'Brest'),
        ('Gomel', 'Gomel'),
        ('Grodno', 'Grodno'),
        ('Mogilev', 'Mogilev'),
        ('Vitebsk', 'Vitebsk'),
    ]
    city = forms.ChoiceField(choices=CITIES, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2", "date_of_birth", "phone_number"]

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('You must be at least 18 years old to register.')

        return dob


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Choices from 1 to 5

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ['rating', 'text']


from django.test import TestCase
from .forms import RegisterForm
from datetime import date, timedelta

class RegisterFormTest(TestCase):
    def test_register_form_valid(self):
        form = RegisterForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'date_of_birth': (date.today() - timedelta(days=365*20)).strftime('%Y-%m-%d'),  # 20 years old
            'phone_number': '+375 (29) 123-45-67',
            'city': 'Minsk'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        form = RegisterForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'date_of_birth': date.today().strftime('%Y-%m-%d'),  # Today's date, i.e., less than 18 years old
            'phone_number': '+375 (29) 123-45-67',
            'city': 'Minsk'
        })
        self.assertFalse(form.is_valid())