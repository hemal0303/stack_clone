from django.contrib.auth.decorators import login_required
from django.db.models import Case, F, IntegerField, Sum, When
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from home.views import index

from .forms import QuestionForm
from .models import Post, Vote, Tags


# Create your views here.
@login_required(login_url="/login/")
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
            question = form.save(commit=False)
            question.author_id = request.user.id
            question.save()
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
            vote_count = (
                Vote.objects.filter(question_id=question_id)
                .values("question_id")
                .annotate(
                    positive_votes=Sum(
                        Case(
                            When(vote_type="up", then=1),
                            default=0,
                            output_field=IntegerField(),
                        )
                    ),
                    negative_votes=Sum(
                        Case(
                            When(vote_type="down", then=1),
                            default=0,
                            output_field=IntegerField(),
                        )
                    ),
                )
            )
            if vote_count:
                vote_count = vote_count.aggregate(
                    total=F("positive_votes") - F("negative_votes")
                )
            if request.user.id:
                voted = (
                    Vote.objects.filter(
                        question_id=question_id, user_id=request.user.id
                    )
                    .values("vote_type")
                    .first()
                )
        return render(
            request,
            "blogs/view_question.html",
            context={
                "data": data,
                "vote_count": vote_count["total"] if vote_count else 0,
                "voted": voted["vote_type"] if voted else None,
            },
        )
    except Exception as e:
        print("Error", e)


@login_required(login_url="/login/")
def delete_question(request, question_id):
    try:
        if question_id:
            Post.objects.filter(id=int(question_id)).update(is_deleted=True)
            return redirect(index)
    except Exception as e:
        print("Error", e)


@csrf_exempt
def vote_question(request, question_id):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"code": 401, "msg": "Unauthorised access"})
        if request.method == "POST":
            vote_count = 0
            current_user_id = request.user.id
            new_vote_type = request.POST.get("vote_type")
            voted = False
            if question_id:
                post_owner = (
                    Post.objects.filter(id=question_id).values("author_id").first()
                )
                if post_owner["author_id"] == current_user_id:
                    return JsonResponse(
                        {"code": 0, "msg": "You cant vote your own question"}
                    )
                existing_vote = (
                    Vote.objects.filter(question=question_id, user_id=current_user_id)
                    .values("vote_type")
                    .first()
                )
                if not existing_vote:
                    Vote.objects.create(
                        question_id=question_id,
                        user_id=current_user_id,
                        vote_type=new_vote_type,
                    )
                    voted = True
                if (
                    existing_vote
                    and existing_vote["vote_type"] == "up"
                    and new_vote_type == "up"
                ):
                    Vote.objects.filter(
                        question=question_id, user_id=current_user_id
                    ).delete()
                    voted = False
                elif (
                    existing_vote
                    and existing_vote["vote_type"] == "down"
                    and new_vote_type == "up"
                ):
                    Vote.objects.filter(
                        question=question_id, user_id=current_user_id
                    ).update(vote_type=new_vote_type)
                    voted = True
                elif (
                    existing_vote
                    and existing_vote["vote_type"] == "up"
                    and new_vote_type == "down"
                ):
                    Vote.objects.filter(
                        question=question_id, user_id=current_user_id
                    ).update(vote_type=new_vote_type)
                    voted = True
                elif (
                    existing_vote
                    and existing_vote["vote_type"] == "down"
                    and new_vote_type == "down"
                ):
                    Vote.objects.filter(
                        question=question_id, user_id=current_user_id
                    ).delete()
                    voted = False
                else:
                    pass
                vote_count = (
                    Vote.objects.filter(question_id=question_id)
                    .values("question_id")
                    .annotate(
                        positive_votes=Sum(
                            Case(
                                When(vote_type="up", then=1),
                                default=0,
                                output_field=IntegerField(),
                            )
                        ),
                        negative_votes=Sum(
                            Case(
                                When(vote_type="down", then=1),
                                default=0,
                                output_field=IntegerField(),
                            )
                        ),
                    )
                )
                if len(vote_count) >= 1:
                    vote_count = vote_count.aggregate(
                        total=F("positive_votes") - F("negative_votes")
                    )
                    vote_count = vote_count["total"]
                else:
                    vote_count = str(0)
                return JsonResponse(
                    {"code": 1, "vote_count": str(vote_count), "voted": voted}
                )
        return JsonResponse({"code": 0, "msg": "Something went wrong"})
    except Exception as e:
        print("Error", e)


def search_tags(request):
    try:
        if request.method == "POST":
            input_tags = request.POST.get("input_tags")
            response = []
            if input_tags:
                tags = Tags.objects.filter(name__icontains=input_tags).values(
                    "id", "name", "description"
                )[:6]
                for tag in tags:
                    response.append(
                        {
                            "id": tag["id"],
                            "name": tag["name"],
                            "description": tag["description"],
                        }
                    )
            return JsonResponse({"code": 1, "data": response})
        return JsonResponse({"code": 0, "msg": "Something went wrong"})
    except Exception as e:
        print("Error", e)
