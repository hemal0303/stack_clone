from django.shortcuts import render, redirect
from .forms import QuestionForm
from django.contrib import messages
from .models import Post, PostAnswer, Tags


# Create your views here.
def post_question(request, question_id):
    try:
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author_id = request.user.id
                question.save()
                messages.success(request, "Question has been posted.")
                return redirect(view_question, question_id=question.id)

        form = QuestionForm()
        return render(request, "blogs/post_question.html", context={"form": form})
    except Exception as e:
        print("Error", e)


def view_question(request, question_id):
    try:
        if question_id:
            Post.objects.filter(id=question_id).values("title", "body").first()
            return render(request, "blogs/view_question.html", context={})
    except Exception as e:
        print("Error", e)
