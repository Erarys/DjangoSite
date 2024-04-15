from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import PersonalPage, RegisterView, UpdatePersonalPage

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(
            template_name="myauth/logout.html"
        ),
        name="logout",
    ),
    path("profile/", PersonalPage.as_view(), name="profile"),
    path("profile/update", UpdatePersonalPage.as_view(), name="update_profile"),
    path("register/", RegisterView.as_view(), name="register"),
]
