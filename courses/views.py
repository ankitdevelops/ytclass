from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
from .models import *
from profiles.models import Profile
from django.urls import reverse
from django.http import HttpResponse
from .forms import *
from pytube import Playlist, YouTube
from django.forms import inlineformset_factory


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


def explore_courses(request):
    all_courses = Course.objects.all()
    context = {
        "all_courses": all_courses,
    }
    return render(request, "courses/explore.html", context)


def course_details(request, id):
    course = get_object_or_404(Course, pk=id)
    lectures = (
        Lecture.objects.all().filter(lecture_of_course=course).order_by("created")
    )
    context = {
        "lectures": lectures,
        "course": course,
    }

    return render(request, "courses/course_details.html", context)


def course_dashboard(request, id):
    course = get_object_or_404(Course, pk=id)
    lectures = (
        Lecture.objects.all().filter(lecture_of_course=course).order_by("created")
    )
    context = {
        "lectures": lectures,
        "course": course,
    }
    return render(request, "courses/course_dashboard.html", context)


def add_course(request):
    user = request.user
    profile = request.user.profile
    course_form = AddCourseForm()
    if profile.is_instructor:
        if request.method == "POST":
            course_form = AddCourseForm(request.POST, request.FILES)
            if course_form.is_valid():
                course = course_form.save(commit=False)
                course.instructor = user
                course.save()
                return redirect(reverse("course_dashboard", kwargs={"id": course.id}))

    context = {
        "course_form": course_form,
    }

    return render(request, "courses/add_course.html", context)


def delete_course(request,id):
    course = get_object_or_404(Course, pk=id)
    course.delete()
    return redirect(reverse("profile"))


def edit_course(request, id):
    course = get_object_or_404(Course, pk=id)
    user = Profile.objects.get(user=request.user)
    edit_form = EditCourseForm(instance=course)
    instructor_of_course = course.instructor
    if user.is_instructor:
        if instructor_of_course == request.user:
            if request.method == "POST":
                edit_form = EditCourseForm(request.POST, request.FILES, instance=course)
                if edit_form.is_valid():
                    messages.success(request, f"{course.title} successfully Updated")
                    edit_form.save()
                    return redirect(
                        reverse("course_dashboard", kwargs={"id": course.id})
                    )
    else:
        edit_form = EditCourseForm(instance=course)
    context = {
        "edit_form": edit_form,
        "course": course,
    }

    return render(request, "courses/edit_course.html", context)


def add_lecture(request, id):
    course = Course.objects.get(id=id)
    # add_lecture = AddLectureForm()
    LectureFormSet = inlineformset_factory(
        Course,
        Lecture,
        form=AddLectureForm,
        extra=3,
        fields=("lecture_title", "youtube_video_id"),
        can_delete=False,
    )
    formset = LectureFormSet(queryset=Lecture.objects.none(), instance=course)

    if request.method == "POST":
        # add_lecture = AddLectureForm(request.POST)
        formset = LectureFormSet(request.POST, instance=course)
        if formset.is_valid():
            # lecture = formset.save(commit=False)
            # lecture.lecture_of_course = course
            formset.save()
            # add_lecture = AddLectureForm()
            return redirect(reverse("course_dashboard", kwargs={"id": course.id}))

    context = {
        "add_lecture": formset,
        "course": course,
    }

    return render(request, "courses/add_lecture.html", context)


def edit_lecture(request, id):
    lecture = get_object_or_404(Lecture, pk=id)
    course = lecture.lecture_of_course
    user = Profile.objects.get(user=request.user)
    edit_form = EditLectureForm(instance=lecture)
    instructor_of_course = course.instructor
    if user.is_instructor:
        if instructor_of_course == request.user:
            if request.method == "POST":
                edit_form = EditLectureForm(request.POST, instance=lecture)
                if edit_form.is_valid():
                    messages.success(
                        request, f"{lecture.lecture_title} successfully Updated"
                    )
                    edit_form.save()
                    return redirect(
                        reverse("course_dashboard", kwargs={"id": course.id})
                    )
    else:
        edit_form = EditLectureForm(instance=lecture)
    context = {
        "edit_form": edit_form,
        "course": course,
    }
    return render(request, "courses/edit_lecture.html", context)


def delete_lecture(request, id):
    lecture = get_object_or_404(Lecture, pk=id)
    course = lecture.lecture_of_course
    lecture.delete()

    context = {
        "course": course,
    }
    return redirect(reverse("course_dashboard", kwargs={"id": course.id}))


def dashboard(request):
    instructor = Profile.objects.get(user=request.user)
    if instructor.is_instructor:
        course_by_instructor = Course.objects.filter(instructor=request.user)
    else:
        return redirect("home")
    context = {
        "course_by_instructor": course_by_instructor,
    }
    return render(request, "courses/dashboard.html", context)


def enroll_course(request, id):
    course = get_object_or_404(Course, pk=id)
    lectures = (
        Lecture.objects.all().filter(lecture_of_course=course).order_by("created")
    )
    instructor = Profile.objects.get(user=course.instructor)
    if request.method == "POST":
        # enroll_button = request.POST["enroll"]
        course = get_object_or_404(Course, pk=id)
        if course.enrolled_student.filter(id=request.user.id).exists():
            pass
        else:
            course.enrolled_student.add(request.user)
            messages.success(request, "Enrolled successfully")
        enrollment, created = Enrollment.objects.get_or_create(
            enrolled_by=request.user, course_id=id
        )
        if created:
            course.save()
            enrollment.save()
            return redirect(reverse("enroll", kwargs={"id": course.id}))

    context = {
        "course": course,
        "lectures": lectures,
        "instructor": instructor,
    }

    return render(request, "courses/learn_page.html", context)


def mark_complete(request):
    print(request)
    id = request.POST.get("id")
    user = request.user
    if request.method == "POST":
        lecture = get_object_or_404(Lecture, pk=id)
        if lecture.completed.filter(id=user.id).exists():
            lecture.completed.remove(user)
        else:
            lecture.completed.add(user)
            lecture.save()

    return HttpResponse("Marked Completed")


def auto_import(request, id):
    course = Course.objects.get(id=id)
    video_links = Playlist(course.playlist_link).video_urls

    for link in video_links:
        lecture = Lecture.objects.bulk_create(
            [
                Lecture(
                    lecture_of_course=course,
                    lecture_title=YouTube(link).title,
                    youtube_video_id=link.split("=")[1],
                )
            ]
        )
    return redirect(reverse("course_dashboard", kwargs={"id": course.id}))
