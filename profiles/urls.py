from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("update/update_profile/", views.edit_profile, name="update_profile"),
    path(
        "instructor/<str:username>/",
        views.instructor_profile,
        name="instructor_profile",
    ),
    path("become_instructor/", views.become_instructor_form, name="become_instructor"),
]
