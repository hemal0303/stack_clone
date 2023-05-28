from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from home.elastic_connection import ElasticSearch
from django.conf import settings
import pytz
import datetime

es = settings.ELASTICSEARCH_CONNECTION


def validate_entry(value):
    count = MaintenanceMode.objects.all().count()
    if count >= 1:
        raise ValidationError("This table can have only one Entry!!")


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=250)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = RichTextField()
    published_on = models.DateTimeField(null=True, blank=True)
    drafted_on = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    votes = models.BigIntegerField(default=0)
    tags = models.ManyToManyField("Tags")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ("-published_on",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        utc_now = datetime.datetime.now(pytz.utc)
        self.created = utc_now
        super().save(*args, **kwargs)

        # Elasticsearch
        index_available = False
        while not index_available:
            if es.indices.exists(index="posts"):
                index_available = True
                body = {
                    "id": self.id,
                    "title": self.title,
                    "author_id": self.author.id,
                    "author_name": self.author.first_name + " " + self.author.last_name,
                    "body": self.body,
                }
                instance_bool = es.exists(index="posts", id=self.id)
                if instance_bool:
                    instance = es.get(index="posts", id=self.id)
                    instance["_source"]["title"] = self.title
                    instance["_source"]["body"] = self.body
                    source_to_update = {
                        "doc": {
                            "title": self.title,
                            "body": self.body,
                        }
                    }
                    es.update(index="posts", id=self.id, body=source_to_update)
                else:
                    es.index(index="posts", body=body, id=self.id)
            else:
                mapping = {
                    "id": {"type": "integer"},
                    "title": {"type": "text"},
                    "author_id": {"type": "integer"},
                    "author_name": {"type": "text"},
                    "body": {"type": "text"},
                }
                es.indices.create(
                    index="posts", body={"mappings": {"properties": mapping}}
                )


class Tags(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class MaintenanceMode(models.Model):
    name = models.CharField(max_length=50, default="maintenance_entry")
    status = models.BooleanField(default=False, validators=[validate_entry])


class PostAnswer(models.Model):
    question = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = RichTextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.question.title)


class Comment(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(
        PostAnswer, on_delete=models.CASCADE, null=True, blank=True
    )


class Vote(models.Model):
    VOTE_TYPE = (
        ("up", "Up"),
        ("down", "Down"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    vote_type = models.CharField(choices=VOTE_TYPE, max_length=20)

    def __str__(self):
        return str(self.question.title)
