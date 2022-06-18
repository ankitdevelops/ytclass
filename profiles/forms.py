from .models import Profile, Become_Instructor
from django import forms


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user", "is_instructor", "avatar"]


class BecomeInstructorForm(forms.ModelForm):
    class Meta:
        model = Become_Instructor
        exclude = ["user"]
