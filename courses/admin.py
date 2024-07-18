from django.contrib import admin

from catalogue.models import CourseStudents, CourseTeachers, CourseAssistants, Tag
from .models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseStudents)
admin.site.register(CourseTeachers)
admin.site.register(CourseAssistants)
admin.site.register(Tag)
admin.site.register(Section)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Quiz)
admin.site.register(AnswerSets)
admin.site.register(Question)
admin.site.register(Choice)
