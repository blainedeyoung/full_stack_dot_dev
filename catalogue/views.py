from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from catalogue.filters import CourseFilter
from catalogue.models import Tag
from courses.models import Course


def course_list(request):
    f = CourseFilter(request.GET, queryset=Course.objects.all())
    return render(request, 'catalogue/course_list.html', {'filter': f})


class TagListView(ListView):
    model = Tag
    template_name = 'catalogue/tag_list.html'
    context_object_name = 'tags'


class TagCreateView(CreateView):
    model = Tag
    template_name = 'catalogue/tag_create.html'
    fields = ['name', 'priority']
    success_url = reverse_lazy('catalogue:tag-list')


class TagUpdateView(UpdateView):
    model = Tag
    template_name = 'catalogue/tag_update.html'
    fields = ['name', 'priority']
    success_url = reverse_lazy('catalogue:tag-list')


class TagDeleteView(DeleteView):
    model = Tag
    template_name = 'catalogue/tag_delete.html'
    success_url = reverse_lazy('catalogue:tag-list')
