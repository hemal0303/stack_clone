from django.urls import path

from . import views

urlpatterns = [
    path("post_question/<int:question_id>/", views.post_question, name="post_question"),
    path("view_question/<int:question_id>/", views.view_question, name="view_question"),
    path("delete_question/<int:question_id>/",views.delete_question,name="delete_question"),
]
