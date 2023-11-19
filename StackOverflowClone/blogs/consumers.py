import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from home import manager
from django.http import JsonResponse, HttpResponse
import logging
import json


class BlogConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.accept()
            self.question_name = (
                self.scope["url_route"]["kwargs"]["question_name"]
                if "question_name" in self.scope["url_route"]["kwargs"]
                else None
            )
            self.socket_question_name = (
                "chat_%s" % self.question_name
                if self.question_name is not None
                else None
            )
            if self.socket_question_name is not None:
                async_to_sync(self.channel_layer.group_add)(
                    self.socket_question_name, self.channel_name
                )

            self.user_id = (
                self.scope["url_route"]["kwargs"]["user_id"]
                if "user_id" in self.scope["url_route"]["kwargs"]
                else None
            )
            self.socket_user_id = (
                "connection_%s" % self.user_id if self.user_id is not None else None
            )
            if self.socket_user_id is not None:
                async_to_sync(self.channel_layer.group_add)(
                    self.socket_user_id, self.channel_name
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
        if self.socket_question_name is not None:
            async_to_sync(self.channel_layer.group_send)(
                self.socket_question_name,
                {"type": "chat_message", "message": message, "user_id": user_id},
            )
        if self.socket_user_id is not None:
            async_to_sync(self.channel_layer.group_send)(
                self.socket_user_id,
                {
                    "type": "chat_message",
                    "message": message,
                    "user_id": self.socket_user_id,
                },
            )

    def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        self.send(
            text_data=json.dumps(
                {"type": "chat", "message": message, "user_id": user_id}
            )
        )


class WebhookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = f"GitHub Webhook called: {data}"
        await self.send(text_data=json.dumps({"message": message}))
