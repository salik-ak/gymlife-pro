from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from .forms import RegistrationForm,UserForm
from django.contrib.auth import get_user_model
from django.contrib import messages
# for email verification
# from gymlife.home.utils import send_forgotpassword_mail
from home.utils import send_activation_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse


# Create your views here.
def user_login(request):
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
            return redirect(user_login)

    return render(request,'user_login.html')

def user_signup(request):  
    form =   RegistrationForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['username']
        phone=form.cleaned_data['phone']
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
       
    
        User    =   get_user_model()
        if User.objects.filter(email=email).exists():
            print('email allready taken')
            return redirect('user_signup')
        elif User.objects.filter(phone=phone).exists():
            print('phone number allready taken')
            return redirect('user_signup')
        else:
            user= User.objects.create_user(username=name,phone=phone,email=email,password=password)
            # user.phone=phone
            setattr(user, 'phone', phone)
            user.save()
            # EditProfile.objects.create(user=user)


            #sending email-helper function in utils
            send_activation_email(request,user)
            messages.success(request, "We have send you an email ,please verify it")
            return redirect('/authentication/user_login/?command=verification&email='+email)
       
    else:
        form   = RegistrationForm()
    context =   {
        'form' : form,
    }
    return render(request,'user_signup.html',context)

def user_logout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    messages.success(request,'successfully loged out')

    return redirect('/')

# def forgotPassword(request):
#     if request.method=='POST':
#         email= request.POST['email']
#         if CustomUser.objects.filter(email=email).exists():
#             user=CustomUser.objects.get(email__iexact=email) 
#             send_forgotpassword_mail(request,user,email)
#             messages.success(request,"Paswword reset email has been sent")
#             return redirect('signin')
#         else:
#             messages.error(request,"Account doesnot exist")
#             return redirect('forgotPassword')
#     return render(request,'accounts/forgotPassword.html')


# def user_signup(request):
#     if 'email' in request.session:
#         return redirect('home')
#     if request.method == 'POST':
        
#         username = request.POST['username']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 == password2:
#             if CustomUser.objects.filter(email=email).exists():
#                 print('email allready taken')
#                 return redirect('user_signup')
#             elif CustomUser.objects.filter(phone=phone).exists():
#                 print('phone number allready taken')
#                 return redirect('user_signup')
#             else:
#                 user = CustomUser.objects.create_user(
#                     phone=phone, password=password1, email=email,  username=username
#                 )
#                 user.save()
#                 #user activation
#                 current_site = get_current_site(request)
#                 mail_subject = 'please activate your account'
#                 message = render_to_string('account_verification_email.html',{
#                     'user' : user,
#                     'domain': current_site,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': default_token_generator.make_token(user),

#                 })
#                 to_email = email
#                 send_email = EmailMessage(mail_subject,message,to=[to_email])
#                 send_email.send()
#                 message.success(request,'registration successful.')
#                 # return redirect('signup')

#                 print('user created')

#             return redirect('user_login')
#         else:
#             print('password not matching')
#             return redirect('user_signup')

#     else:
#         return render(request, 'user_signup.html')
    

def activate(request,uidb64,token):
   try:
    uid =urlsafe_base64_decode(uidb64).decode()
    user= CustomUser._default_manager.get(pk=uid)
   except(TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
    user=None

   if user is not None and default_token_generator.check_token(user,token):
    user.is_active=True
    user.save()
    messages.success(request,'account activated')
    return redirect('user_login')
   else:
    messages.error(request,"invalid activation link")
    return redirect('user_signup')
