from django.contrib import admin
from .models import ErrorBase


class ErroBaseInstance(admin.ModelAdmin):
    model = ErrorBase
    list_display = ["class_name", "level", "message", "traceback", "created_on"]


admin.site.register(ErrorBase, ErroBaseInstance)
