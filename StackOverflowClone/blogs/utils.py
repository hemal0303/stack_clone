from django.db.models import Q
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginatePost(request, posts, results):
    if not results:
        results = 5
    page = request.GET.get("page")
    paginator = Paginator(posts, results)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    leftIndex = int(page) - 1
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, posts
