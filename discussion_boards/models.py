from django.db import models
from django.utils.text import slugify
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()


class DiscussionBoard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    date_created = models.DateField(auto_now_add=True)
    last_commented_on = models.DateField(auto_now=True)
    course = models.OneToOneField(to=Course, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='course_for_board')

    # in the edit method, make sure that changing the name also changes the slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Board(models.Model):
    discussion_board = models.ForeignKey(to=DiscussionBoard, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=50)
    user_views = models.ManyToManyField(to=User, through='UserViews', related_name="user_views", blank=True)

    def __str__(self):
        return self.title


class UserViews(models.Model):
    user_viewed = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_viewed")
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name="board")
    last_viewed = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    parent_comment = models.ForeignKey(to="Comment", null=True, related_name="parent_c", on_delete=models.CASCADE)
    parent_board = models.ForeignKey(to=Board, on_delete=models.CASCADE, related_name="parent_b")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="author")
    subject = models.CharField(max_length=100)
    comment_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_edited = models.DateTimeField(auto_now=True)
    votes = models.ManyToManyField(to=User, through='UserVote', blank=True)

    def __str__(self):
        return self.subject

    # save() also saves parent_board to update last_viewed
    def save(self, **kwargs):
        parent_b = Board.objects.get(id=self.parent_board)
        parent_b.save()
        super().save()


class UserVote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_votes")
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE,
                                related_name="comment_voted_on")
    vote_choices = (
        ("u", "Up"),
        ("d", "Down"),
    )
    vote = models.CharField(max_length=5, choices=vote_choices)
