from django.shortcuts import render,redirect
from trainer.forms import RegistrationForm
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from trainer.models import Trainer
from course.models import Course
# from .models import TrainerProfile
# from .forms import ProfileForm



#email verification
from home.utils import send_activation_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse

# Create your views here.

def trainer_login(request):
    if 'email' in request.session:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            request.session['email'] =email
            auth.login(request,user)
            return redirect('home')
        else:
            return redirect('trainer_login')

    return render(request,'trainer_login.html')

def trainer_signup(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            name = form.cleaned_data['username']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            specialized_course_id = form.cleaned_data['specialized_course']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            certificates = form.cleaned_data['certificates']  # Access the file using cleaned_data
            profile_pictures = form.cleaned_data['profile_pictures']

            if Trainer.objects.filter(email=email).exists():
                print('Email already taken')
                return redirect('trainer_signup')
            elif Trainer.objects.filter(phone=phone).exists():
                print('Phone number already taken')
                return redirect('trainer_signup')
            else:
                try:
                    specialized_course_id = form.cleaned_data['specialized_course'].id
                    specialized_course = Course.objects.get(id=specialized_course_id)
                    
                    user = Trainer.objects.create(
                        username=name,
                        phone=phone,
                        email=email,
                        password=password,
                        specialized_course=specialized_course,  # Assign the Course instance
                        age=age,
                        gender=gender,
                        certificates=certificates,
                        profile_pictures = profile_pictures
                        
                    )
                    user.save()
                    return redirect('home')
                except Course.DoesNotExist:
                    print('Invalid specialized course ID')
                    return redirect('trainer_signup')
    else:
        form = RegistrationForm()
    return render(request, 'trainer_signup.html', {'form': form})

def trainer(request):
    trainer = Trainer.objects.all()
    context ={
        'trainer': trainer
    }
    return render (request,'trainers.html',context)





# def update_trainer_profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             profile = form.save()
#             # Redirect to a success page or do further processing
#             return redirect('success_page')
#     else:
#         form = ProfileForm()
    
#     context = {
#         'form': form
#     }
#     return render(request, 'profile_form.html', context)











def trainer_profile(request):
    # try:
    #     trainer_profile = TrainerProfile.objects.select_related('user').get(user__username=username)
    # except TrainerProfile.DoesNotExist:
    #     # Handle the case when the trainer profile doesn't exist
    #     trainer_profile = None

    # context = {
    #     'trainer_profile': trainer_profile
    # }
    return render(request, 'trainer_profile.html')


# def trainer_signup(request):
#     print('hello')  
#     form =   RegistrationForm(request.POST)
#     print('koiii')
#     if form.is_valid():
#         name = form.cleaned_data['username']
#         phone=form.cleaned_data['phone']
#         email=form.cleaned_data['email']
#         password=form.cleaned_data['password']
#         specialized_course=form.cleaned_data['specialized_course']
    
#         print('hai bro')
#         if Trainer.objects.filter(email=email).exists():
#             print('email allready taken')
#             return redirect('trainer_signup')
#         elif Trainer.objects.filter(phone=phone).exists():
#             print('phone number allready taken')
#             return redirect('trainer_signup')
#         else:
#             print('vallathum nadakkuo')
#             user= Trainer.objects.create(username=name,phone=phone,email=email,password=password)
#            
#             user.save()
#             print('hello')
#             return redirect('trainer_login')
#             # EditProfile.objects.create(user=user)


#             # #sending email-helper function in utils
#             # send_activation_email(request,user)
#             # messages.success(request, "We have send you an email ,please verify it")
#             # return redirect('/trainer/trainer_login/?command=verification&email='+email)
       
#     else:
#         form   = RegistrationForm()
#     context =   {
#         'form' : form,
#     }
#     return render(request,'trainer_signup.html',context)


