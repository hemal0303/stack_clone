from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blogs.models import Post, Tags
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Create 1000 records with random text for the Post model"

    def handle(self, *args, **options):
        author_id = 21
        tag_id = 9
        status = "published"
        tag = Tags.objects.get(id=tag_id)
        for _ in range(100000):
            title = get_random_string(length=10)
            body = get_random_string(length=100)
            post = Post(title=title, body=body, author_id=author_id, status=status)
            post.save()
            post.tags.add(tag)

        self.stdout.write(self.style.SUCCESS("Successfully created 1000 records"))
