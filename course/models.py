from django.db import models
from django.urls import reverse

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='course')
    description = models.TextField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)
    duration = models.DateField(null=True)

    def get_url(self):
        return reverse('course_details',args=[self.id])
    
    def __str__(self):
        return self.course_name
