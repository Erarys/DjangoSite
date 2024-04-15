from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from shop.models import Basket


class PersonalPage(TemplateView):
    template_name = 'myauth/personal_page.html'

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        kwargs["baskets"] = Basket.objects.all()
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs


class UpdatePersonalPage(UpdateView):
    template_name = "myauth/update_profile.html"
    model = User
    fields = "username", "first_name", "last_name", "email"
    success_url = reverse_lazy("myauth:profile")

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy("myauth:profile")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response
