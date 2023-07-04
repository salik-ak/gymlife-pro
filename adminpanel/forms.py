from django import forms
from course.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'slug', 'price', 'image', 'description','duration']
        labels = {

            'course_name': 'course_name',
            'slug': 'slug',
            'price': 'price',
            'image': 'image',
            'description': 'description',
            'duration'  : 'duration'
        }

class DateInput(forms.DateInput):
    input_type = 'date'