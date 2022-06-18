from django.urls import path
from . import views

urlpatterns = [
    path(
        "category/<slug:category_slug>/",
        views.explore_courses,
        name="course_by_category",
    ),
    path("course_details/<str:id>/", views.course_details, name="course_details"),
    path("explore/", views.explore_courses, name="explore"),
    path("enroll/<str:id>/", views.enroll_course, name="enroll"),
    path("mark-complete/", views.mark_complete, name="mark-complete"),
    path("add_course/", views.add_course, name="add-course"),
    path("delete_course/<str:id>/", views.delete_course, name="delete-course"),
    path("edit_course/<str:id>/", views.edit_course, name="edit-course"),
    path("dashboard/<str:id>/", views.course_dashboard, name="course_dashboard"),
    path("add_lecture/<str:id>/", views.add_lecture, name="add-lecture"),
    path("edit_lecture/<str:id>/", views.edit_lecture, name="edit-lecture"),
    path("delete_lecture/<str:id>/", views.delete_lecture, name="delete-lecture"),
    path("auto_import/<str:id>/", views.auto_import, name="auto-import"),
    path("search/", views.search, name="search"),
]
