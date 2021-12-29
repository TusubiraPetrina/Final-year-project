from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from helpers.email import PasswordConfirm, PasswordReset, ConfirmAccount
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
    #    "activate/",
    #    ConfirmAccount.as_view(),
    #    name="confirm_account",
    #),
    path(
        "reset_password/",
        PasswordConfirm.as_view(),
        name="reset_password",
    ),
    url(r"^activate/(?P<eToken>[0-9A-Za-z_\-]+)/(?P<refreshID>[0-9A-Za-z]+)/$", ConfirmAccount),
]
