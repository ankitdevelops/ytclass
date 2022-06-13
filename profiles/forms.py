from .models import Profile
from django import forms


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user", "is_instructor"]
