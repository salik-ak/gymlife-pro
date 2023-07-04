from django.shortcuts import render
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import auth
from django.contrib import messages
from authentication.models import CustomUser
from adminpanel.forms import CourseForm
from course.models import Course
from trainer.models import Trainer
from authentication.models import Notification

# Create your views here.
def adminlogin(request):

    if 'email' in request.session:
        return redirect('adminhome')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_superuser:
            request.session['email'] = email
            auth.login(request, user)
            print('admin logged in ')
            messages.success(request, 'successfully signed up!')
            return redirect('adminhome')
        else:
            print('Not autherised')
            messages.error(request, 'Not autherised')
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')

def adminhome(request):
    
    return render(request, 'admin_home.html')

def admin_userlist(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }

    return render(request, 'adminclient_list.html', context)

def blockuser(request,id):
    user = CustomUser.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request,'user successfully blocked')
    else:
        user.is_active = True
        user.save()
        messages.success(request,'user successfully unblocked')
    return redirect('admin_userlist')


def delete_user(request,id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    return redirect('admin_userlist')





def admincourse(request):
    course = Course.objects.all()
    context = {
        'course': course
    }
    return render(request, 'admin_course_list.html', context)

def admin_add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_course_list')
        else:
            return redirect('admin_add_course')
    else:
        form = CourseForm()
        context = {
            'form': form
        }
    return render(request, 'admin_add_course.html', context)

def block_course(request,id):
    course = Course.objects.get(id=id)
    if course.is_available:
        course.is_available = False
        course.save()
        messages.success(request,'course successfully blocked')
    else:
        course.is_available = True
        course.save()
        messages.success(request,'course successfully unblocked')
    return redirect('admin_course_list')



def delete_course(request,id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect('admin_course_list')
    


def admin_trainers_list(request):
    trainers = Trainer.objects.all()
    context = {
        'trainers': trainers
    }
    return render(request,'admin_trainers_list.html',context)


def block_trainer(request,id):
    trainer = Trainer.objects.get(id=id)
    if trainer.is_active:
        trainer.is_active = False
        trainer.save()
        messages.success(request,'trainer successfully blocked')
    else:
        trainer.is_active = True
        trainer.save()
        messages.success(request,'trainer successfully unblocked')
    return redirect('admin_trainers_list')
   
def delete_trainer(request,id):
    trainer = Trainer.objects.get(id=id)
    trainer.delete()
    return redirect('admin_trainers_list')


def notification(request):

    user_notifications = Notification.objects.filter(user=request.user, is_read=False)
    context={
        'notifications': user_notifications
        }
    return render(request, 'admin_dashbord.html',context)

    



def adminlogout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    return redirect('adminlogin')