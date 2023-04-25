from django.contrib import messages
from django.db.models import Case, F, IntegerField, Sum, When
from django.shortcuts import redirect, render
from home.views import index

from .forms import QuestionForm
from .models import Post, Vote


# Create your views here.
def post_question(request, question_id):
    post = Post.objects.get(id=question_id) if question_id != 0 else None
    if post:
        form = QuestionForm(instance=post)
    else:
        form = QuestionForm(request.POST)
    if request.method == "POST":
        form = (
            QuestionForm(request.POST, instance=post)
            if post
            else QuestionForm(request.POST)
        )
        if form.is_valid():
            print("request.user.id", request.user.id)
            question = form.save(commit=False)
            question.author_id = request.user.id
            question.save()
            messages.success(request, "Question has been updated.")
            return redirect(view_question, question_id=question.id)

    return render(
        request,
        "blogs/post_question.html",
        context={"form": form, "question_id": question_id if question_id else 0},
    )


def view_question(request, question_id):
    try:
        if question_id:
            vote_count = None
            voted = False
            data = (
                Post.objects.filter(id=question_id)
                .values("id", "title", "body", "votes")
                .first()
            )
            vote_count = Vote.objects.filter(question_id=question_id).values("question_id").annotate(
                positive_votes=Sum(Case(When(vote_type='up', then=1), default=0, output_field=IntegerField())),
                negative_votes=Sum(Case(When(vote_type='down', then=1), default=0, output_field=IntegerField())))
            if vote_count:
                vote_count = vote_count.aggregate(total=F('positive_votes') - F("negative_votes"))
            if request.user.id:
                voted = Vote.objects.filter(question_id=question_id, user_id=request.user.id).values("vote_type").first()
                print("voted", voted)
        return render(request, "blogs/view_question.html", context={"data": data, "vote_count": vote_count['total'] if vote_count else 0,
                                                                    "voted": voted['vote_type'] if voted else None})
    except Exception as e:
        print("Error", e)


def delete_question(request, question_id):
    try:
        if question_id:
            Post.objects.filter(id=int(question_id)).update(is_deleted=True)
            messages.success(request, "Question has been deleted.")
            return redirect(index)
    except Exception as e:
        print("Error", e)
