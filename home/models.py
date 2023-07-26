from django.db import models
from django.urls import reverse
from authentication.models import CustomUser
from trainer.models import Trainer
from course.models import Course

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100,blank=True)
    order_id = models.CharField(max_length=100,blank=True,default='empty')
    payment_method = models.CharField(max_length=100,blank=True)
    amount_paid = models.FloatField(default=0)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code_image = models.BinaryField(null=True, blank=True)


    def __str__(self):
        return self.order_id
    

class MembershipPlan(models.Model):
    plan =models.CharField(max_length=50)
    price = models.IntegerField()
    def __str__(self):
        return str(self.plan)


class Subscription(models.Model):
    STATUS = (
        ('subscribed', 'subscribed'),
        ('Cancelled','Cancelled'),
        
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    trainer= models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=15)
    price_total = models.ForeignKey( MembershipPlan,on_delete=models.CASCADE, null=True)
    age = models.CharField(max_length=50)
    refrence = models.CharField(max_length=50, blank=True)
    payment_status = models.CharField(max_length=30)
    status = models.CharField(max_length=50, choices=STATUS, default='subscription Confirmed')
    is_subscribed = models.BooleanField(default=False)
    subscription_number = models.CharField(max_length=20)
    DueDate=models.DateTimeField(blank=True,null=True)
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True,)
    is_active =  models.BooleanField(default=True)
    
    def __str__(self):
        return self.user
    
class PurchasedCourse(models.Model):
    client=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE)
    selected_plan = models.ForeignKey(MembershipPlan,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.client


class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=50)

class userProfile(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=False)
    age = models.CharField(max_length=3)
    profile_picture = models.ImageField(upload_to='profile_pictures')
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.user




class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    exercises = models.ManyToManyField(Exercise, through='WorkoutPlanExercise')

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('workout_plan_detail',args=[self.id])
    
class WorkoutPlanExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.workout_plan.name} - {self.exercise.name}'



