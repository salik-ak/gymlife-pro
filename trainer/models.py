from django.db import models
from authentication.models import CustomUser
from course.models import Course
from django.urls import reverse

class Trainer(models.Model):
    username = models.CharField(null=False,max_length=50)
    email = models.EmailField(blank=False,max_length=50,unique=True)
    phone =models.CharField(unique=True,max_length=12)
    password = models.CharField(max_length=50)
    specialized_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    age = models.IntegerField(blank=False)
    gender = models.CharField(max_length=10)
    certificates = models.ImageField(upload_to='certificate', null=True)
    profile_pictures = models.ImageField(upload_to='profile_pictures')
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.username
    
    def get_url(self):
        return reverse('enrollment',args=[self.id])
    


    



class TrainerProfile(models.Model):
    user = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    specialized_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    bio = models.TextField()
    experience = models.PositiveIntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    address = models.TextField()
    

    def __str__(self):
        return self.user.username
    

    

        
