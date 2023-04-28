from django.contrib import messages

# Create your views here.
from django.contrib.auth import login
from django.shortcuts import redirect, render

from blogs.models import Post

from .backend import EmailAuthBackend
from .forms import NewUserForm


def index(request):
    try:
        questions = (
            Post.objects.filter(is_deleted=False)
            .values("title", "tags__name", "id", "body")
            .order_by("id")
            .distinct("id")
        )
        return render(request, "home/content.html", {"questions": questions})
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
