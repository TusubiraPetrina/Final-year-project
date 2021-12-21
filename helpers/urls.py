from django.contrib import admin
from django.urls import path, include

from helpers.email import PasswordConfirm, PasswordReset
from .login import LoginView, RegisterView, LogoutView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/", 
        LogoutView.as_view(), 
        name="sign_out",
        ),
    path(
        "register/",
        RegisterView.as_view(),
        name="sign_up",
    ),
    path(
        "forgot_password/",
        PasswordReset.as_view(),
        name="forgot_password",
    ),
    #path(
    #    "password_token/",
    #    PasswordConfirm.as_view(),
    #    name="password_token",
    #),
    path(
        "reset_password/",
        PasswordConfirm.as_view(),
        name="reset_password",
    ),
]
