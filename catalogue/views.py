from django.shortcuts import render
from django.views.generic import ListView, View
from catalogue.models import Category, Tag
from courses.models import Course


class CourseListView(ListView):
    model = Course
    template_name = 'catalogue/course_list.html'
    context_object_name = 'courses'
    # paginate_by = 10


class CategoryTagView(View):

    def get(self, request):
        course_selected = request.GET.get('course')
        courses = Course.objects.prefetch_related('categories', 'tags').all()
        context = {
            'courses': courses,
            'categories': Category.objects.all(), #names instead
            'tags': Tag.objects.all()
        }
        return render(request, 'catalogue/category_tag.html', context)

