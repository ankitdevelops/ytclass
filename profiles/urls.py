from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("update_profile/", views.edit_profile, name="update_profile"),
    path("<str:username>/", views.instructor_profile, name="instructor_sprofile"),
]
