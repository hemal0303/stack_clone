from django.urls import include, path, re_path

from . import consumers

ws_urlpatterns = [
    path("ws/home/", consumers.BlogConsumer.as_asgi()),
    re_path(
        r"ws/question/(?P<chat_box_name>\w+)/$",
        consumers.BlogConsumer.as_asgi(),
    ),
]
