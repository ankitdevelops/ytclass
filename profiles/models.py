from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    avatar = models.ImageField(
        upload_to="avatar/%Y/%m/",
        default="default.png",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    )  # TODO: Chage to url field
    is_instructor = models.BooleanField(default=False)
    headline = models.CharField(max_length=50)  # TODO: change to bio
    biography = models.TextField()  # TODO: change to about me
    city = models.CharField(
        max_length=50, blank=True, null=True
    )  # TODO:chage to location
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(user_signed_up)
def new_user_signup(
    sender,
    sociallogin,
    **kwargs,
):
    p = Profile(user=kwargs["user"])
    user = SocialAccount.objects.filter(user=kwargs["user"])
    if sociallogin.account.provider == "github":
        p.full_name = user.values()[0]["extra_data"]["name"]
        p.headline = user.values()[0]["extra_data"]["company"]
        p.biography = user.values()[0]["extra_data"]["bio"]
        p.github = user.values()[0]["extra_data"]["html_url"]
        p.website = user.values()[0]["extra_data"]["blog"]
        p.city = user.values()[0]["extra_data"]["location"]
        # p.avatar = user.values()[0]["extra_data"]["avatar_url"]

    if sociallogin.account.provider == "google":
        p.full_name = user.values()[0]["extra_data"]["name"]
        # p.avatar = user.values()[0]["extra_data"]["picture"]
    p.save()
