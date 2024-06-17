from django.shortcuts import render
from django.views import View


# Create your views here.
class DiscussionBoardView(View):
    def get(self, request, **kwargs):
        if not self.kwargs:
            return render(request, template_name="discussion_boards/site_board.html")
