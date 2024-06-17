from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the courses index.")


class CourseDetailView(View):
    def get(self, request, course):
        context = {
            "object": Course.objects.select_related('discussion_board')
            .prefetch_related('categories', 'tags', 'students', 'teachers', 'assistants',
                              'course_sections__section_lessons').get(slug=course)}
        return render(request, 'courses/course_detail.html', context)


class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/course_create.html'
    fields = ['name', 'description', 'required_classes', 'categories', 'tags', 'version', 'teachers', 'assistants']
    success_url = reverse_lazy("catalogue:course-list")


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/course_update.html'
    fields = ['name', 'description', 'required_classes', 'categories', 'tags', 'version', 'teachers', 'assistants']
    success_url = reverse_lazy("catalogue:course-list")


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_delete.html'
    success_url = reverse_lazy("catalogue:course-list")


class SectionCreateView(CreateView):
    model = Section
    template_name = 'courses/section_create.html'
    fields = ['title']

    #associates the section with the course
    def form_valid(self, form):
        course_slug = self.kwargs['course']
        course = Course.objects.get(slug=course_slug)
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        course_slug = self.kwargs['course']
        return reverse_lazy('courses:course-detail', kwargs={'course': course_slug})


class SectionUpdateView(UpdateView):
    model = Section
    template_name = 'courses/section_update.html'
    fields = ['title']

    def get_object(self, queryset=None):
        course_slug = self.kwargs['course']
        section_number = self.kwargs['number']
        return get_object_or_404(Section, course__slug=course_slug, number=section_number)

    def get_success_url(self):
        course_slug = self.kwargs['course']
        return reverse_lazy('courses:course-detail', kwargs={'course': course_slug})


class SectionDeleteView(DeleteView):
    model = Section
    template_name = 'courses/section_delete.html'
    success_url = reverse_lazy("catalogue:course-list")

    def get_object(self, queryset=None):
        course_slug = self.kwargs['course']
        section_number = self.kwargs['number']
        return get_object_or_404(Section, course__slug=course_slug, number=section_number)

    def get_success_url(self):
        course_slug = self.kwargs['course']
        return reverse_lazy('courses:course-detail', kwargs={'course': course_slug})


class LessonCreateView(CreateView):
    model = Lesson
    fields = ['title', 'lesson_type', 'lesson_text', 'attached_file']
    template_name = 'courses/lesson_create.html'

    def form_valid(self, form):
        course_slug = self.kwargs['course']
        section_number = self.kwargs['section_number']
        section = Section.objects.get(course__slug=course_slug, number=section_number)
        form.instance.section = section
        return super().form_valid(form)

    def get_success_url(self):
        course_slug = self.kwargs['course']
        return reverse_lazy('courses:course-detail', kwargs={'course': course_slug})


class LessonUpdateView(UpdateView):
    model = Lesson
    template_name = 'courses/lesson_update.html'
    fields = ['title', 'lesson_type', 'lesson_text', 'attached_file']

    def get_object(self, queryset=None):
        course_slug = self.kwargs['course']
        section_number = self.kwargs['section_number']
        lesson_number = self.kwargs['number']
        return get_object_or_404(Lesson, section__course__slug=course_slug, section__number=section_number,
                                 number=lesson_number)

    def get_success_url(self):
        course_slug = self.kwargs['course']
        return reverse_lazy('courses:course-detail', kwargs={'course': course_slug})


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'courses/lesson_delete.html'
    success_url = reverse_lazy("catalogue:course-list")

    def get_object(self, queryset=None):
        course_slug = self.kwargs['course']
        section_number = self.kwargs['section_number']
        lesson_number = self.kwargs['number']
        return get_object_or_404(Lesson, section__course__slug=course_slug, section__number=section_number,
                                 number=lesson_number)

    def get_success_url(self):
        course_slug = self.kwargs['course']
        return reverse_lazy('courses:course-detail', kwargs={'course': course_slug})

