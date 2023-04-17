from django.shortcuts import render
from .forms import QuestionForm
from django.contrib import messages


# Create your views here.
def post_question(request):
    print("request", request.method)
    try:
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author_id = request.user.id
                question.save()
                messages.success(request, "Question has been posted.")
        form = QuestionForm()
        return render(request, "blogs/post_question.html", context={"form": form})
    except Exception as e:
        print("Error", e)
