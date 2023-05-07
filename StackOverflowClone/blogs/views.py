from django.contrib.auth.decorators import login_required
from django.db.models import Case, F, IntegerField, Sum, When
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from home import manager
from home.views import index
import logging
from .forms import QuestionForm, AnswerForm
from .models import Post, Vote, Tags, PostAnswer
from blogs.utils import paginatePost


# Create your views here.
@login_required(login_url="/login/")
def post_question(request, question_id):
    try:
        post = Post.objects.get(id=question_id) if question_id != 0 else None
        tag_response = []
        search_tags = []
        if post:
            form = QuestionForm(instance=post)
            tags = post.tags.all().values("id", "name")
            if tags:
                for tag in tags:
                    tag_response.append({"id": tag["id"], "name": tag["name"]})
        else:
            form = QuestionForm(request.POST)
        if request.method == "POST":
            form = (
                QuestionForm(request.POST, instance=post)
                if post
                else QuestionForm(request.POST)
            )
            if form.is_valid():
                search_tags = request.POST.getlist("search_tag[]")
                question = form.save(commit=False)
                question.author_id = request.user.id
                question.save()
                question.tags.set(search_tags)
                return redirect(view_question, question_id=question.id)

        return render(
            request,
            "blogs/post_question.html",
            context={
                "form": form,
                "question_id": question_id if question_id else 0,
                "tags": tag_response,
            },
        )
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


def view_question(request, question_id):
    try:
        user_id = request.user.id
        if question_id:
            vote_count = None
            voted = False
            data = Post.objects.filter(id=question_id).first()
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
            answer_data = PostAnswer.objects.filter(question_id=question_id).values(
                "id",
                "question",
                "body",
                "author",
                "author__first_name",
                "author__last_name",
                "updated_at",
                "is_accepted",
                "created_at",
            )
        return render(
            request,
            "blogs/view_question.html",
            context={
                "data": data,
                "vote_count": vote_count["total"] if vote_count else 0,
                "voted": voted["vote_type"] if voted else None,
                "answer_data": answer_data,
                "total_answer": len(answer_data),
                "login_user_id": user_id,
                "question_id": question_id,
            },
        )
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


@login_required(login_url="/login/")
def delete_question(request, question_id):
    try:
        if question_id:
            Post.objects.filter(id=int(question_id)).update(is_deleted=True)
            return redirect(index)
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


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
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


def search_tags(request):
    try:
        if request.method == "POST":
            input_tags = request.POST.get("input_tags")
            response = []
            if input_tags:
                tags = Tags.objects.filter(name__icontains=input_tags).values(
                    "id", "name"
                )[:10]
                for tag in tags:
                    response.append(
                        {
                            "id": tag["id"],
                            "name": tag["name"],
                        }
                    )
            return JsonResponse({"code": 1, "data": response})
        return JsonResponse({"code": 0, "msg": "Something went wrong"})
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


@login_required(login_url="/login/")
def tags_list(request):
    try:
        pagesize = request.GET.get("pagesize")
        tags = Tags.objects.all()
        custom_range, tags = paginatePost(request, tags, pagesize)

        return render(
            request,
            "blogs/tags.html",
            {
                "tags": tags,
                "custom_range": custom_range,
                "pagesize": pagesize,
            },
        )
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


@login_required(login_url="/login/")
def answer_form(request, question_id, answer_id):
    try:
        answer = PostAnswer.objects.get(id=answer_id) if answer_id != 0 else None
        question = (
            Post.objects.filter(id=question_id).values("title", "body", "id").first()
        )
        form = AnswerForm(instance=answer)
        if question_id:
            return render(
                request,
                "blogs/post_answer.html",
                context={"form": form, "question": question, "answer_id": answer_id},
            )
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


@login_required(login_url="/login/")
def post_answer(request, question_id, answer_id):
    try:
        if request.method == "POST":
            answer = PostAnswer.objects.get(id=answer_id) if answer_id != 0 else None
            search_tag = request.POST.get("search_tag")
            form = (
                AnswerForm(request.POST, instance=answer)
                if answer
                else AnswerForm(request.POST)
            )
            if form.is_valid():
                answer = form.save(commit=False)
                answer.question_id = question_id
                answer.author_id = request.user.id
                answer.save()
                return redirect(view_question, question_id=question_id)
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


@login_required(login_url="/login/")
def accept_answer(request):
    try:
        if request.method == "POST":
            question_id = request.POST.get("question_id")
            answer_id = request.POST.get("answer_id")
            is_accepted = request.POST.get("is_accepted")
            old_answer_id = 0
            if question_id is None or answer_id is None:
                return JsonResponse({"code": 0, "msg": "Something went wrong"})
            fields = {"is_accepted": False if is_accepted == "true" else True}
            print("fields", fields)
            PostAnswer.objects.filter(question_id=question_id, id=answer_id).update(
                **fields
            )
            old_answer = (
                PostAnswer.objects.filter(question_id=question_id, is_accepted=True)
                .exclude(id=answer_id)
                .first()
            )
            if old_answer:
                old_answer.is_accepted = False
                old_answer.save()
                old_answer_id = old_answer.id
            return JsonResponse({"code": 1, "old_answer_id": old_answer_id})
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")
