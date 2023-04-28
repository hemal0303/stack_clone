from django.contrib import messages

# Create your views here.
from django.contrib.auth import login
from django.shortcuts import redirect, render

from blogs.documents import PostDocument
from blogs.models import Post

from .backend import EmailAuthBackend
from .forms import NewUserForm


def index(request):
    try:
        question_search = request.GET.get("question_search")
        search_fields = {}
        questions = []
        if question_search:
            elastic_data = PostDocument.search().query("match", title=question_search)
            print("elastic_data", elastic_data)
            for post in elastic_data:
                questions.append(
                    {
                        "id": post.id,
                        "title": post.title,
                        "body": post.body,
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
                # .distinct("id")
            )
            print("used query")
        return render(request, "home/content.html", {"questions": questions, "question_search": question_search})
    except Exception as e:
        print("Error", e)


def authcheck(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        backend = EmailAuthBackend()
        user = backend.authenticate(request, email=email, password=password)
        if user:
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
