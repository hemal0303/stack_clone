from django.contrib import admin

from .models import Comment, MaintenanceMode, Post, PostAnswer, Tags, Vote

admin.site.register(Post)
admin.site.register(PostAnswer)
admin.site.register(Tags)
admin.site.register(MaintenanceMode)
admin.site.register(Vote)
admin.site.register(Comment)
