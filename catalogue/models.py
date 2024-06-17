from django.db import models
from courses.models import Course
from accounts.models import User


class CourseStudents(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='courses_enrolled_in')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='enrolled_students')
    enrollment_date = models.DateField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)


class CourseTeachers(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='teachers_for_course')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='courses_teaching')
    participation_start = models.DateField(auto_now_add=True)
    participation_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class CourseAssistants(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='assistants_for_course')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='courses_assistant_for')
    participation_start = models.DateField(auto_now_add=True)
    participation_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class Category(models.Model):
    class Meta:
        ordering = ['priority']

    name = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField(default=0)


class Tag(models.Model):
    class Meta:
        ordering = ['priority']

    name = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField(default=0)
