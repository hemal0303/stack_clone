from django.shortcuts import render
from .models import Profile
from home import manager
import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from PIL import Image

# Create your views here.


def profile_search(request):
    try:
        all_users = Profile.objects.filter().values(
            "avatar",
            "location",
            "about_me",
            "user__email",
            "user",
            "user__first_name",
            "user__last_name",
            "user__username",
            "github_link",
            "website_link",
            "twitter_link",
        )
        return render(request, "users/profiles.html", context={"data": all_users})
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


def profile(request):
    try:
        user_id = request.user.id
        if user_id:
            user_data = (
                Profile.objects.filter(user_id=user_id)
                .values(
                    "user_id",
                    "user__first_name",
                    "user__last_name",
                    "user__email",
                    "user__username",
                    "github_link",
                    "website_link",
                    "twitter_link",
                    "avatar",
                    "location",
                    "about_me",
                )
                .first()
            )
            return render(request, "users/profile.html", context={"data": user_data})
        else:
            return render(request, "users/profile.html")
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")


def save_profile(request, user_id):
    try:
        profile_img = request.FILES["profile_img"]
        img_name = "profile_avatars/" + str(profile_img.name).strip()
        firstname = request.POST.get("first_name", "")
        lastname = request.POST.get("last_name", "")
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        location = request.POST.get("location", "")
        about_me = request.POST.get("about_me", "")
        website_link = request.POST.get("website_like", "")
        twitter_link = request.POST.get("twitter_link", "")
        github_link = request.POST.get("github_link", "")
        fs = FileSystemStorage()
        filename = fs.save(f"profile_avatars/{profile_img.name}", profile_img)

        basewidth = 315
        img_path = fs.path(filename)
        img = Image.open(img_path)
        wpercent = basewidth / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(img_path)

        User.objects.filter(id=user_id).update(
            first_name=firstname, last_name=lastname, email=email, username=username
        )
        Profile.objects.filter(user_id=user_id).update(
            avatar=img_name,
            github_link=github_link,
            twitter_link=twitter_link,
            website_link=website_link,
        )

        messages.success(request, "Profile Updated.")
        return redirect(profile)
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")
