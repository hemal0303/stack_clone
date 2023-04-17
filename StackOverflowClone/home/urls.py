from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.authcheck, name="login"),
    path("register/", views.register, name="register"),
]
