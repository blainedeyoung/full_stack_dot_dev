import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from courses.mixins import NumberedModelMixin

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    required_classes = models.ManyToManyField(to='Course', blank=True)
    categories = models.ManyToManyField(to='catalogue.Category', blank=True)
    tags = models.ManyToManyField(to='catalogue.Tag', blank=True)
    version = models.CharField(max_length=30)
    date_created = models.DateField(auto_now_add=True)
    students = models.ManyToManyField(to=User, through='catalogue.CourseStudents', related_name="students", blank=True)
    teachers = models.ManyToManyField(to=User, through='catalogue.CourseTeachers', related_name="teachers", blank=True)
    assistants = models.ManyToManyField(to=User, through='catalogue.CourseAssistants', related_name="assistants", blank=True)
    discussion_board = models.OneToOneField(to='discussion_boards.DiscussionBoard',
                                            null=True, blank=True, on_delete=models.CASCADE,
                                            related_name='course_discussion')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'version'], name='unique_name_version')
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Section(NumberedModelMixin):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'number'], name='unique_section_course')
        ]

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='course_sections', blank=True)

    def get_number_filter_kwargs(self):
        return {'course': self.course}


class Lesson(NumberedModelMixin):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['section', 'number'], name='unique_lesson_section')
        ]

    lesson_types = (
        ("v", "Video"),
        ("t", "Text"),
        ("q", "Quiz"),
        ("e", "Exercise"),
    )
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE, related_name='section_lessons', blank=True)
    date_created = models.DateField(auto_now_add=True)
    lesson_type = models.CharField(max_length=10, choices=lesson_types)
    attached_file = models.FileField(null=True, blank=True)
    lesson_text = models.TextField(null=True, blank=True)

    def get_number_filter_kwargs(self):
        return {'section': self.section}


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.OneToOneField(to=Lesson, on_delete=models.CASCADE, related_name='video_lesson')
    access_url = models.URLField(max_length=100)
    date_created = models.DateField(auto_now_add=True)


class Quiz(models.Model):
    lesson = models.OneToOneField(to=Lesson, on_delete=models.CASCADE, related_name='quiz_lesson')
    answers = models.ManyToManyField(to=User, through='AnswerSets', related_name="answers", blank=True)


class AnswerSets(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, related_name='answer_sets')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_answers')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    date_made = models.DateTimeField(auto_now_add=True)
    is_key = models.BooleanField(default=False)
    choices = models.CharField(max_length=100)


class Question(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(null=True, blank=True)
    attached_file = models.FileField(null=True, blank=True)


class Choice(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.TextField(null=True, blank=True)
    attached_file = models.FileField(null=True, blank=True)
    letter = models.CharField(max_length=1)
