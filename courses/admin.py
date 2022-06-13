from django.contrib import admin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_slug": ("category",)}


admin.site.register(Category, CategoryAdmin)


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"title_slug": ("title",)}


admin.site.register(Course, CourseAdmin)


class LectureAdmin(admin.ModelAdmin):
    prepopulated_fields = {"lecture_title_slug": ("lecture_title",)}


admin.site.register(Lecture, LectureAdmin)


admin.site.register(Enrollment)
# admin.site.register(Lecture_Status)
