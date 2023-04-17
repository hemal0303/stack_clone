from django.urls import path

from . import views

urlpatterns = [
    path("post_question/", views.post_question, name="post_question"),
]
