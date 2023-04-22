from django.shortcuts import render, redirect
from .forms import QuestionForm
from django.contrib import messages
from .models import Post, PostAnswer, Tags
from home.views import index

# Create your views here.
def post_question(request, question_id):
    try:
        print(question_id,"question_id")
        form = QuestionForm()
        if question_id:
            post = Post.objects.get(id=question_id)
            form = QuestionForm(instance=post)
        if request.method == "POST":
            print("post----------------",request.user.id)
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author_id = 1
                question.save()
                messages.success(request, "Question has been posted.")
                return redirect(view_question, question_id=question.id)
        
        
        return render(request, "blogs/post_question.html", context={"form": form})
    except Exception as e:
        print("Error", e)


def view_question(request, question_id):
    try:
        if question_id:
            data = Post.objects.filter(id=question_id).values("title", "body").first()
            print("data",data)
            return render(request, "blogs/view_question.html", context={"data":data})
    except Exception as e:
        print("Error", e)


def delete_question(request,question_id):
    try:
        print("question_id", question_id)
        if question_id:
            Post.objects.filter(id=int(question_id)).update(id_delted=True)
            messages.success(request, "Question has been deleted.")
            return redirect(index)
    except Exception as e:
        print("Error", e)