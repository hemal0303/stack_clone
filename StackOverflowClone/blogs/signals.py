from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Post
from elasticsearch import Elasticsearch

es = Elasticsearch()


@receiver(post_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
    instance_bool = es.exists(index="posts", id=instance.id)
    if instance_bool:
        es.delete(index="posts", id=instance.id)
