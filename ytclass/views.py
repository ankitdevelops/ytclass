from courses.models import Course
from django.shortcuts import render
from django.db.models import Count


def home(request):
    featured_courses = Course.objects.all().filter(is_featured=True)
    most_enrolled = Course.objects.annotate(
        enroll_count=Count("enrolled_student")
    ).order_by("-enroll_count")[:6]
    recently_added = Course.objects.all().order_by("-created")[:6]
    context = {
        "featured_courses": featured_courses,
        "most_enrolled": most_enrolled,
        "recently_added": recently_added,
    }
    return render(request, "webpages/home.html", context)


def about(request):
    return render(request, "webpages/about.html")
