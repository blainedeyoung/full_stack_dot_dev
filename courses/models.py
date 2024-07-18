import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from courses.mixins import NumberedModelMixin

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    required_classes = models.ManyToManyField(to='Course', blank=True)
    tags = models.ManyToManyField(to='catalogue.Tag', blank=True)
    version = models.CharField(max_length=30)
    date_created = models.DateField(auto_now_add=True)
    students = models.ManyToManyField(to=User, through='catalogue.CourseStudents', related_name="enrolled_courses",
                                      blank=True)
    teachers = models.ManyToManyField(to=User, through='catalogue.CourseTeachers', related_name="courses_teacher_for",
                                      blank=True)
    assistants = models.ManyToManyField(to=User, through='catalogue.CourseAssistants',
                                        related_name="courses_assistant_in", blank=True)
    discussion_board = models.OneToOneField(to='discussion_boards.DiscussionBoard',
                                            null=True, blank=True, on_delete=models.CASCADE,
                                            related_name='parent_course')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'version'], name='unique_name_version')
        ]

    def __str__(self):
        return f"{self.name} - v.{self.version}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}-{self.version}")
        #is_new true if this is a new instance being created
        is_new = self._state.adding
        if not is_new:
            #if the name or version of the course has changed, update the associated discussion board
            old_course = Course.objects.get(id=self.id)
            if old_course.name != self.name or old_course.version != self.version:
                self.discussion_board.name = self.name
                self.discussion_board.version = self.version
                self.discussion_board.save()
        super().save(*args, **kwargs)

        #if a new instance is being created, create a new discussion board
        if is_new:
            from discussion_boards.models import DiscussionBoard
            discussion_board = DiscussionBoard.objects.create(name=self.name, version=self.version, course=self)
            self.discussion_board = discussion_board
            super().save(update_fields=['discussion_board'])


class Section(NumberedModelMixin):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'number'], name='unique_section_course')
        ]

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='sections', blank=True)

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
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE, related_name='lessons', blank=True)
    date_created = models.DateField(auto_now_add=True)
    lesson_type = models.CharField(max_length=10, choices=lesson_types)
    attached_file = models.FileField(null=True, blank=True)
    lesson_text = models.TextField(null=True, blank=True)

    def get_number_filter_kwargs(self):
        return {'section': self.section}


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.OneToOneField(to=Lesson, on_delete=models.CASCADE, related_name="video")
    access_url = models.URLField(max_length=100)
    date_created = models.DateField(auto_now_add=True)


class Quiz(models.Model):
    lesson = models.OneToOneField(to=Lesson, on_delete=models.CASCADE, related_name='quiz')
    answers = models.ManyToManyField(to=User, through='AnswerSets', related_name="quiz", blank=True)


class AnswerSets(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, related_name='answer_sets')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='quiz_answers')
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
