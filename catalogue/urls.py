from django.urls import path
from . import views

app_name = "catalogue"
urlpatterns = [
    path("", views.course_list, name="course-list"),
    path("tag/", views.TagListView.as_view(), name="tag-list"),
    path("tag-create/", views.TagCreateView.as_view(), name="tag-create"),
    path("tag-update/<int:pk>", views.TagUpdateView.as_view(), name="tag-update"),
    path("tag-delete/<int:pk>", views.TagDeleteView.as_view(), name="tag-delete"),
]
