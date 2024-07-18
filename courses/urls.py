from django.urls import path
from . import views

app_name = "courses"
urlpatterns = [
    path("course-create/", views.CourseCreateView.as_view(), name="course-create"),
    path("course-update/<slug:slug>/", views.CourseUpdateView.as_view(), name="course-update"),
    path("course-delete/<slug:slug>/", views.CourseDeleteView.as_view(), name="course-delete"),
    path("course/<slug:course>/section/section-create/", views.SectionCreateView.as_view(), name="section-create"),
    path("course/<slug:course>/section/<int:number>/section-update/", views.SectionUpdateView.as_view(),
         name="section-update"),
    path("course/<slug:course>/section/<int:number>/section-delete/", views.SectionDeleteView.as_view(),
         name="section-delete"),
    path("course/<slug:course>/section/<int:section_number>/lesson/lesson-create/", views.LessonCreateView.as_view(),
         name="lesson-create"),
    path("course/<slug:course>/section/<int:section_number>/lesson/<int:number>/lesson-update/",
         views.LessonUpdateView.as_view(), name="lesson-update"),
    path("course/<slug:course>/section/<int:section_number>/lesson/<int:number>/lesson-delete",
         views.LessonDeleteView.as_view(), name="lesson-delete"),
    path("<slug:course>/", views.CourseDetailView.as_view(), name="course-detail"),
]
