import django_filters
from django.db import models
from courses.models import Course


class CourseFilter(django_filters.FilterSet):
    tag_name = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name', 'tag_name',]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                }
            },
        }

    @staticmethod
    def filter_by_tag_name(queryset, value):
        return queryset.filter(tags__name__icontains=value)
