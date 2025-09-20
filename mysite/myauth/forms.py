from django import forms
from django.contrib.auth.forms import UserCreationForm

from myauth.models import User


class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email"]
        field_classes = {"email": forms.EmailField}


class EmailUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]