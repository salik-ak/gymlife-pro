from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from course.models import Course
from trainer.models import Trainer

# Create your views here.
def index(request):

    return render(request,'index.html')

def about_us(request):

    return render(request,'about-us.html')

@login_required(login_url='user_login')
def enrollment(request,id):
    user = request.user
    try:
        
        trainer = Trainer.objects.get(pk=id)
        
        purchased_course = trainer.specialized_course

    except Trainer.DoesNotExist:
        
        return redirect('courses')
    context={
        'user' :user,
        'trainer' : trainer,
        'purchased_course ':purchased_course
        
    }


    return render(request,'enrollment.html',context)



def user_profile(request):
    # try:
    #     trainer_profile = TrainerProfile.objects.select_related('user').get(user__username=username)
    # except TrainerProfile.DoesNotExist:
    #     # Handle the case when the trainer profile doesn't exist
    #     trainer_profile = None

    # context = {
    #     'trainer_profile': trainer_profile
    # }
    return render(request, 'user_profile.html')



