from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from shop.models import Order


User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class OrderForm(ModelForm):

    class Meta:
        """форма для добавления дела"""
        model = Order
        fields = ('city', 'address', 'shipping_method', 'comment')
