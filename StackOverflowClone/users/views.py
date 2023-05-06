from django.shortcuts import render
from .models import Profile
from home import manager
import logging
from django.http import JsonResponse, HttpResponse
# Create your views here.

def profile_search(request):
    try:
        all_users = Profile.objects.filter().values("avatar","user__email","user","user__first_name","user__last_name","user__username","github_link","website_link","twitter_link")
        return render(request,"users/profiles.html",context={"data":all_users})
    except Exception as e:
        manager.create_from_exception(e)
        logging.exception("Something went worng.")
        return HttpResponse("Something went wrong")