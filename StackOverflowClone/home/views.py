from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .backend import EmailAuthBackend
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.
from django.contrib.auth import login


def index(request):
    try:
        return render(request, "home/content.html")
    except Exception as e:
        print("Error", e)


def authcheck(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        backend = EmailAuthBackend()
        user = backend.authenticate(request, email=email, password=password)
        if user:
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
