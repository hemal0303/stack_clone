from django.urls import path, include

from . import views

urlpatterns = [
    path("profile_search/", views.profile_search, name="profile_search"),
]
