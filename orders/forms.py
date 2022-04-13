from django import forms
from django.db.models import fields
from .models import Order, Payment
from orders import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'city', 'postcode', 'zilla', 'division', 'order_note']
