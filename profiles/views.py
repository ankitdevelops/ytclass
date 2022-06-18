from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ProfileUpdateForm, BecomeInstructorForm
from django.contrib import messages
from courses.models import Course, Enrollment
from django.urls import reverse

# Create your views here.


@login_required(login_url="account_login")
def profile(request):
    current_user = request.user
    instructor = Profile.objects.get(user=current_user)
    if instructor.is_instructor:
        course_by_instructor = Course.objects.filter(instructor=current_user)
    else:
        course_by_instructor = []
    user_profile = Profile.objects.get(user=current_user)
    enrolled_courses = Enrollment.objects.all().filter(enrolled_by=current_user)
    context = {
        "user_profile": user_profile,
        "enrolled_courses": enrolled_courses,
        "course_by_instructor": course_by_instructor,
    }
    return render(request, "profiles/Profile.html", context)


@login_required(login_url="account_login")
def edit_profile(request):
    current_user = request.user
    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile Updated Successfully !!!")
            return redirect("profile")

    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "profile_form": profile_form,
    }

    return render(request, "profiles/edit_profile.html", context)


def instructor_profile(request, username):
    instructor_profile = User.objects.get(username=username)
    instructor_courses = Course.objects.all().filter(instructor=instructor_profile)

    context = {
        "instructor_profile": instructor_profile,
        "instructor_courses": instructor_courses,
    }

    return render(request, "profiles/instructor_profile.html", context)


def become_instructor_form(request):
    form = BecomeInstructorForm()
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = BecomeInstructorForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.user = request.user.profile
            user_profile.is_instructor = True
            user_profile.save()
            user.save()
            messages.success(request, "You are now Instructor")
            return redirect(
                reverse(
                    "profile",
                )
            )

    context = {
        "form": form,
    }

    return render(request, "profiles/become_instructor.html", context)
