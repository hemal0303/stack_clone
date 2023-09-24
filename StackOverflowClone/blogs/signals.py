from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Post, Notification
from elasticsearch import Elasticsearch

es = Elasticsearch()


@receiver(post_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
    instance_bool = es.exists(index="posts", id=instance.id)
    if instance_bool:
        es.delete(index="posts", id=instance.id)


def create_notification(post_id, sender, receiver, type, content):
    if sender == receiver:
        pass
    else:
        Notification.objects.create(
            post_id=post_id,
            sender_id=sender,
            receiver_id=receiver,
            notification_type=type,
            notification_content=content,
        )
