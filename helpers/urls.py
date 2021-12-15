from django.contrib import admin
from django.urls import path, include
from .login import LoginView, RegisterView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='sign_out'), 
    path('register/', RegisterView.as_view(), name='sign_up'),
]