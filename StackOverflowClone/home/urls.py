from django.urls import path,include

from . import views

from django.contrib.auth import views as auth_view

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.authcheck, name="login"),
    path("register/", views.register, name="register"),
    path("signout/", views.signout, name="signout"),
    path("social-auth/", include('social_django.urls', namespace='social')),
    path("logout/", auth_view.LogoutView.as_view(),name="logout"),

]
