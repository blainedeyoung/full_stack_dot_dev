from django.urls import path
from . import views

app_name = "catalogue"
urlpatterns = [
    path("", views.CourseListView.as_view(), name="course-list"),
    path("categories&tags/", views.CategoryTagView.as_view(), name="category-tag"),
]
