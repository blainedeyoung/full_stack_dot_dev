from django.urls import path

from . import views

app_name = "discussion_boards"
urlpatterns = [
    path("<slug:slug>/", views.DiscussionBoardView.as_view(), name="discussion-board"),
    path("board/<int:pk>", views.BoardView.as_view(), name="board"),
    path("<slug:slug>/create-board/", views.CreateBoardView.as_view(), name="create-board"),
    path("board/<int:pk>/update-board/", views.UpdateBoardView.as_view(), name="update-board"),
    path("board/<int:pk>/delete-board/", views.DeleteBoardView.as_view(), name="delete-board"),
    path("comment/view-comment/<int:pk>/", views.ViewCommentView.as_view(), name="view-comment"),
    path("comment/<int:board_id>/create-comment/", views.CreateCommentView.as_view(), name="create-comment"),
    path("comment/create-comment/<int:parent_comment_id>/", views.CreateCommentView.as_view(), name="create-reply"),
    path("comment/update-comment/<int:pk>/", views.UpdateCommentView.as_view(), name="update-comment"),
    path("comment/delete-comment/<int:pk>/", views.DeleteCommentView.as_view(), name="delete-comment"),
]
