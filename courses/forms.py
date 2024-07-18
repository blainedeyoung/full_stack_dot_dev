from django import forms
from accounts.models import User
from catalogue.models import Tag
from .models import Course


class CourseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=forms.CheckboxSelectMultiple,
                                          required=False)
    teachers = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              required=False)
    assistants = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False)
    required_classes = forms.ModelMultipleChoiceField(queryset=Course.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple,
                                                      required=False)

    class Meta:
        model = Course
        fields = ['name', 'description', 'required_classes', 'tags', 'version', 'teachers', 'assistants']
