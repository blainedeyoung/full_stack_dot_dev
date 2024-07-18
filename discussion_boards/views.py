from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from discussion_boards.models import DiscussionBoard, Board, Comment


class DiscussionBoardView(View):
    """
        Discussion board with list of individual boards
    """
    def get(self, request, slug, **kwargs):
        try:
            context_object = self.get_context_object(slug)
        except DiscussionBoard.DoesNotExist:
            if slug == "site-1":
                DiscussionBoard.create_default_site_board()
            else:
                raise DiscussionBoard.DoesNotExist(f"Discussion board with slug {slug} does not exist")
        return render(request, template_name="discussion_boards/discussion_board/discussion_board.html",
                      context={"object": self.get_context_object(slug)})

    def get_context_object(self, slug):
        boards_with_comment_count = Board.objects.annotate(comment_count=Count("comments"))
        discussion_board = (DiscussionBoard.objects.prefetch_related(Prefetch("boards",
                                                                              queryset=boards_with_comment_count))
                            .get(slug=slug))
        return discussion_board


class BoardView(View):
    """
        Individual board with list of comments
    """

    def get(self, request, pk, **kwargs):
        return render(request, template_name="discussion_boards/board/board.html",
                      context={"object": self.get_context_object(pk)})

    def get_context_object(self, pk):
        comments_with_reply_count = Comment.objects.annotate(reply_count=Count("replies"))
        return (Board.objects.select_related("discussion_board").prefetch_related(Prefetch("comments", queryset=comments_with_reply_count))
                .get(pk=pk))


class CreateBoardView(CreateView):
    model = Board
    fields = ["title"]
    template_name = "discussion_boards/board/create_board.html"

    def form_valid(self, form):
        form.instance.discussion_board = DiscussionBoard.objects.get(slug=self.kwargs["slug"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("discussion_boards:discussion-board", kwargs={"slug": self.kwargs["slug"]})


class UpdateBoardView(UpdateView):
    model = Board
    fields = ["title"]
    template_name = "discussion_boards/board/update_board.html"

    def get_object(self, queryset=None):
        return Board.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self):
        slug = Board.objects.get(pk=self.kwargs["pk"]).discussion_board.slug
        return reverse_lazy("discussion_boards:discussion-board", kwargs={"slug": slug})


class DeleteBoardView(DeleteView):
    model = Board
    template_name = "discussion_boards/board/delete_board.html"

    def get_object(self, queryset=None):
        return Board.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self):
        slug = Board.objects.get(pk=self.kwargs["pk"]).discussion_board.slug
        return reverse_lazy("discussion_boards:discussion-board", kwargs={"slug": slug})


class ViewCommentView(View):
    """
        View individual comment with replies
    """

    def get(self, request, pk, **kwargs):
        return render(request, template_name="discussion_boards/comment/view_comment.html",
                      context={"object": self.get_context_object(pk)})

    def get_context_object(self, pk):
        replies = Comment.objects.filter(parent_comment=pk)
        return Comment.objects.prefetch_related(Prefetch("replies", queryset=replies)).get(id=pk)


class CreateCommentView(CreateView):
    model = Comment
    fields = ["subject", "comment_text"]
    template_name = "discussion_boards/comment/create_comment.html"

    def form_valid(self, form):
        # form.instance.author = self.request.user
        if "parent_comment_id" in self.kwargs:
            form.instance.parent_comment = Comment.objects.get(pk=self.kwargs["parent_comment_id"])
            form.instance.parent_board = form.instance.parent_comment.parent_board
        else:
            form.instance.parent_board = Board.objects.get(pk=self.kwargs["board_id"])
        return super().form_valid(form)

    def get_success_url(self):
        if "parent_comment_id" in self.kwargs:
            return reverse_lazy("discussion_boards:view-comment",
                                kwargs={"pk": self.kwargs["parent_comment_id"]})
        else:
            return reverse_lazy("discussion_boards:board",
                                kwargs={"pk": self.kwargs["board_id"]})


class UpdateCommentView(UpdateView):
    model = Comment
    fields = ["subject", "comment_text"]
    template_name = "discussion_boards/comment/update_comment.html"

    def get_success_url(self):
        if self.object.parent_comment:
            return reverse_lazy("discussion_boards:view-comment",
                                kwargs={"pk": self.object.parent_comment.id})
        else:
            return reverse_lazy("discussion_boards:board",
                                kwargs={"pk": self.object.parent_board.id})


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "discussion_boards/comment/delete_comment.html"

    def get_success_url(self):
        if self.object.parent_comment:
            return reverse_lazy("discussion_boards:view-comment",
                                kwargs={"pk": self.object.parent_comment.id})
        else:
            return reverse_lazy("discussion_boards:board",
                                kwargs={"pk": self.object.parent_board.id})

