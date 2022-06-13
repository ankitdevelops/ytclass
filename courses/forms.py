from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import modelformset_factory


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = (
            "title_slug",
            "instructor",
            "enrolled_student",
            "is_featured",
        )


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = (
            "instructor",
            "enrolled_student",
            "title_slug",
            "is_featured",
        )


class EditLectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = "__all__"
        exclude = ("lecture_of_course", "lecture_title_slug", "completed")


class AddLectureForm(forms.ModelForm):
    class Meta:

        model = Lecture
        fields = "__all__"
        exclude = ("lecture_of_course", "lecture_title_slug", "completed")


# LectureFormSet = modelformset_factory(
#     Lecture, fields=("lecture_title", "youtube_video_id"), max_num=3
# )
