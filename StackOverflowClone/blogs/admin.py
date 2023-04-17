from django.contrib import admin
from .models import Post, PostAnswer, Tags, MaintenanceMode

admin.site.register(Post)
admin.site.register(PostAnswer)
admin.site.register(Tags)
admin.site.register(MaintenanceMode)
