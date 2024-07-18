from django.db import models
from courses.models import Course
from accounts.models import User


class CourseStudents(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)


class CourseTeachers(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    participation_start = models.DateField(auto_now_add=True)
    participation_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class CourseAssistants(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    participation_start = models.DateField(auto_now_add=True)
    participation_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class Tag(models.Model):
    #priority: 0 is the highest priority, "hot," "new," "trending," etc.
    #priority: 1 is the second highest priority, categories like "full stack," "front end," "back end," etc.
    #priority: 2 is the third highest priority, categories like "beginner," "intermediate," "advanced," etc.
    #priority: 3 is the fourth highest priority, categories like "python," "java," "javascript," etc.
    class Meta:
        ordering = ['priority']

    name = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.priority})"
