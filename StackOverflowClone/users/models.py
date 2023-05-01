from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, default="", null=True, blank=True)
    title = models.CharField(max_length=255, default="", null=True, blank=True)
    about_me = models.TextField(blank=True,null=True)
    website_link = models.URLField(max_length=255, blank=True)
    website_link = models.URLField(max_length=255, blank=True)
    twitter_link = models.URLField(max_length=255, blank=True)
    github_link = models.URLField(max_length=255, blank=True)
    avatar = models.ImageField(
        default='profile_avatars/default_user_avatar.png', # default avatar
        upload_to='profile_avatars'
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # create a thumbnail
            img.save(self.avatar.path) # overwrite the larger image