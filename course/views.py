from django.shortcuts import render,redirect
from course.models import Course
from trainer.models import Trainer
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def course(request):
    course = Course.objects.filter(is_available = True).order_by('-id')
    trainer = Trainer.objects.all() 
    context ={
        'course': course,
        'trainer': trainer
    }
    return render(request,'course.html',context)



def course_details(request, id):
     
    try:

        single_course = Course.objects.get(pk=id)
        trainer =Trainer.objects.filter(specialized_course=single_course) 
       
    except ObjectDoesNotExist:
        # Handle the case when the requested Course or Trainer does not exist
        # For example, you can redirect to an error page or show an appropriate message.
        return redirect('course')

    context = {
        'single_course': single_course,
        'trainer': trainer
    }

    return render(request, 'course_details.html', context)





