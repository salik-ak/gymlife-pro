from django import forms
from course.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'slug', 'price', 'image', 'description', 'duration']
        labels = {
            'course_name': 'Course Name',
            'slug': 'Slug',
            'price': 'Price',
            'image': 'Image',
            'description': 'Description',
            'duration': 'Duration'
        }
        widgets = {
            'duration': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }