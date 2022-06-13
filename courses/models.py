from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


class Category(models.Model):
    category = models.CharField(max_length=50)
    category_slug = models.SlugField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category


class Course(models.Model):
    language_choice = (("English", "English"), ("Hindi", "Hindi"))
    level_choice = (
        ("Beginners", "Beginners"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    )
    title = models.CharField(max_length=200)
    title_slug = models.SlugField(max_length=200, unique=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(choices=language_choice, max_length=50)
    thumbnail = models.ImageField(
        default="thumbnail.png",
        upload_to="course/thumbnail/",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
        help_text="Recommended image size is 1200 by 720.",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=level_choice)
    course_introduction_video_id = models.CharField(
        max_length=50,
        unique=True,
    )
    playlist_link = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    no_of_lecture = models.IntegerField()
    enrolled_student = models.ManyToManyField(
        User, blank=True, related_name="enrolled_students"
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def no_of_enrolled(self):
        return self.enrolled_student.count()

    def save(self, *args, **kwargs):

        self.title_slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)


class Lecture(models.Model):
    lecture_of_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecture_title = models.CharField(max_length=200)
    lecture_title_slug = models.SlugField(max_length=200, unique=False)
    youtube_video_id = models.CharField(max_length=100, unique=True)
    # lecture_number = models.IntegerField()
    completed = models.ManyToManyField(User, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lecture_title

    def save(self, *args, **kwargs):
        self.lecture_title_slug = slugify(self.lecture_title)
        super(Lecture, self).save(*args, **kwargs)


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.course_title} enrolled by {self.enrolled_by.email}"
