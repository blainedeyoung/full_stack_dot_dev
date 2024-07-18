from django.db import models
from django.utils.text import slugify
import courses.mixins
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

default_boards = ("Announcements", "General", "Assignments", "Questions", "Resources", "Projects",
                  "Exams", "Feedback", "Off-Topic")


class DiscussionBoard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, unique=True)
    date_created = models.DateField(auto_now_add=True)
    last_commented_on = models.DateField(auto_now=True)
    course = models.OneToOneField(to=Course, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='daughter_discussion_board')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'version'], name='unique_name_version_db')
        ]

    def save(self, new_boards=default_boards, *args, **kwargs):
        self.slug = slugify(f"{self.name}-{self.version}")

        # true if this is a new instance being created, if so create default boards
        is_new = self._state.adding

        super().save(*args, **kwargs)

        # if this is a new instance, create boards for it defaulting to the default_boards tuple above
        if is_new:
            for board in new_boards:
                Board.objects.create(discussion_board=self, title=board)

    @classmethod
    def create_default_site_board(cls):
        discussion_board = DiscussionBoard(name="site", version="1")
        new_boards = ("Announcements", "Specific Classes", "Site Feedback", "Resources", "Projects",
                      "Misc", "Off-Topic")
        discussion_board.save(new_boards=new_boards)


class Board(courses.mixins.NumberedModelMixin):
    discussion_board = models.ForeignKey(to=DiscussionBoard, on_delete=models.CASCADE, related_name='boards')
    user_views = models.ManyToManyField(to=User, through='UserViews', related_name="board_last_viewed", blank=True)

    def get_number_filter_kwargs(self):
        return {"discussion_board": self.discussion_board}


class UserViews(models.Model):
    user_viewed = models.ForeignKey(to=User, on_delete=models.CASCADE)
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE)
    last_viewed = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    parent_comment = models.ForeignKey(to="Comment", null=True, related_name="replies", on_delete=models.CASCADE)
    parent_board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name="comments")
    parent_course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name="all_course_comments",
                                      null=True, blank=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="authored_comments", null=True,
                               blank=True)
    subject = models.CharField(max_length=100)
    comment_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_edited = models.DateTimeField(auto_now=True)
    votes = models.ManyToManyField(to=User, through='UserVote', blank=True)

    def __str__(self):
        return self.subject

    # save() also saves parent_board to update last_viewed
    def save(self, **kwargs):
        parent_b = self.parent_board
        parent_b.save()
        super().save()


class UserVote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    vote_choices = (
        ("u", "Up"),
        ("d", "Down"),
    )
    vote = models.CharField(max_length=5, choices=vote_choices)
