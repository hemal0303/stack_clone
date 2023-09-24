import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from home import manager
from django.http import JsonResponse, HttpResponse
import logging


class BlogConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.accept()
            self.question_name = (
                self.scope["url_route"]["kwargs"]["question_name"]
                if "question_name" in self.scope["url_route"]["kwargs"]
                else None
            )
            self.room_group_name = (
                "chat_%s" % self.question_name
                if self.question_name is not None
                else None
            )
            if self.room_group_name is not None:
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name, self.channel_name
                )
        except Exception as e:
            manager.create_from_exception(e)
            logging.exception("Something went worng.")
            return HttpResponse("Something went wrong")

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        text_data = json.loads(text_data)
        message = text_data["message"]
        user_id = text_data["user_id"]
        if self.room_group_name is not None:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "message": message, "user_id": user_id},
            )

    def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        self.send(
            text_data=json.dumps(
                {"type": "chat", "message": message, "user_id": user_id}
            )
        )
