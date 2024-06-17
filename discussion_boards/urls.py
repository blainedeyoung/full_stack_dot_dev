from django.urls import path
from . import views

app_name = "discussion_boards"
urlpatterns = [
    path("", views.DiscussionBoardView.as_view(), name="discussion-board"),
    path("<slug:slug>/", views.DiscussionBoardView.as_view(), name="class-board")
]
