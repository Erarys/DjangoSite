from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Product, Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_address", "promocode", "user", "products"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].queryset = User.objects.filter(id=user.id, is_active=True)


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "price", "discount", "image"]