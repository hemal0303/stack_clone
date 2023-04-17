from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post

# Create your forms here.


class QuestionForm(ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body")
