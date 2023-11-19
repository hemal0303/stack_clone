from django.urls import include, path, re_path

from . import consumers

ws_urlpatterns = [
    re_path("ws/home/(?P<user_id>\w+)/$", consumers.BlogConsumer.as_asgi()),
    re_path(
        r"ws/question/(?P<question_name>\w+)/$",
        consumers.BlogConsumer.as_asgi(),
    ),
]
