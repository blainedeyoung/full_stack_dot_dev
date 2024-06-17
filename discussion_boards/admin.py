from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(DiscussionBoard)
admin.site.register(Board)
admin.site.register(UserViews)
admin.site.register(Comment)
admin.site.register(UserVote)
