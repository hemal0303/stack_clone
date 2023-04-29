from django.contrib import messages

# Create your views here.
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from blogs.documents import PostDocument
from blogs.models import Post
from .backend import EmailAuthBackend
from .forms import NewUserForm
from blogs.utils import paginatePost


def index(request):
    try:
        pagesize = request.GET.get("pagesize")
        question_search = request.GET.get("question_search")
        search_fields = {}
        questions = []
        if question_search:
            elastic_data = PostDocument.search().query("match", title=question_search)
            for post in elastic_data:
                questions.append(
                    {
                        "id": post.id,
                        "title": post.title,
                    }
                )
            search_fields = {
                "title__icontains": question_search,
            }
        if len(questions) == 0:
            search_fields["is_deleted"] = False
            questions = (
                Post.objects.filter(**search_fields)
                .values("title", "tags__name", "id", "body")
                .order_by("id")
                .distinct("id")
            )
        custom_range, questions = paginatePost(request, questions, pagesize)
        return render(
            request,
            "home/content.html",
            {
                "questions": questions,
                "question_search": question_search,
                "custom_range": custom_range,
                "pagesize": pagesize,
            },
        )
    except Exception as e:
        print("Error", e)


def authcheck(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        backend = EmailAuthBackend()
        user = backend.authenticate(request, email=email, password=password)
        if user:
            logout(request)
            login(request, user, backend="home.backend.EmailAuthBackend")
            messages.success(request, "Logged in Successfully!")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, "home/login.html")


def register(request):
    try:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user, backend="home.backend.EmailAuthBackend")
                messages.success(request, "Your account has been created.")
                return redirect("/")
            else:
                messages.error(request, "Please enter Valid details.")
        form = NewUserForm()
        return render(request, "home/register.html", context={"register_form": form})
    except Exception as e:
        print("Error", e)


def signout(request):
    try:
        request_userId = request.user.id
        logout(request)
        messages.success(request, "Logout Successfully!")
        return redirect("/")

    except Exception as e:
        print("logout error--", e)
