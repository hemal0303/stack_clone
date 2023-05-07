from django.urls import path, include

from . import views

urlpatterns = [
    path("profile_search/", views.profile_search, name="profile_search"),
    path("profile/",views.profile,name="profile"),
    path("save_profile/<int:user_id>/", views.save_profile, name="save_profile"),
]
