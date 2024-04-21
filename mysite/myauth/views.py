from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from shop.models import Basket


# Представление для отображения персональной страницы пользователя
class PersonalPage(TemplateView):
    template_name = 'myauth/personal_page.html'

    def get_context_data(self, **kwargs):
        # Добавляем корзины пользователя в контекст
        kwargs.setdefault("view", self)
        kwargs["baskets"] = Basket.objects.all()
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs


# Представление для обновления профиля пользователя
class UpdatePersonalPage(UpdateView):
    template_name = "myauth/update_profile.html"
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    success_url = reverse_lazy("myauth:profile")

    def get_object(self, queryset=None):
        # Возвращает текущего пользователя как объект для обновления
        return self.request.user


# Представление для регистрации нового пользователя
class RegisterView(CreateView):
    form_class = UserCreationForm  # Используем стандартную форму для регистрации пользователя
    template_name = 'myauth/register.html'
    success_url = reverse_lazy("myauth:profile")

    def form_valid(self, form):
        # Если форма регистрации валидна, создаем нового пользователя
        response = super().form_valid(form)

        # Получаем данные из формы
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        # Аутентифицируем нового пользователя и логиним его сразу после регистрации
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)

        return response
