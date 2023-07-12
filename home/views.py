from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from course.models import Course
from trainer.models import Trainer
from home.models import MembershipPlan,Subscription,Payment
import datetime
from django.http import JsonResponse
import json
from .models import PurchasedCourse
from authentication.models import CustomUser
from django.db.models import Q
from .forms import UserProfileForm
from .models import userProfile
# Create your views here.
def index(request):
    trainer= Trainer.objects.all()
    course = Course.objects.all()
    context ={
        'trainer':trainer,
        'course': course
    }

    return render(request,'index.html',context)



@login_required(login_url='user_login')
def enrollment(request,id):
    try:
        current_user = request.user
        trainer = Trainer.objects.get(pk=id)
        plan = MembershipPlan.objects.all()
        selected_plan = plan.first()
        purchased_course = PurchasedCourse.objects.create(client=current_user,trainer=trainer,selected_plan=selected_plan  )
        purchased_course.save()
    
    except Trainer.DoesNotExist:
        return redirect('courses')
    
    context = {
        'user': current_user,
        'trainer': trainer,
        'plan': plan
    }
    
    return render(request, 'enrollment.html', context)

@login_required(login_url='user_login')
def enrolled(request):
    user1=request.user
    
   
    if request.method == "POST":

        
        
        trainer = request.POST.get('trainer')
        trainer1=Trainer.objects.get(pk=trainer)
       
        
        
        course = request.POST.get('course')
        # selected_course =Trainer.objects.get(id=course)
        member = request.POST.get('member')
        price_plan = MembershipPlan.objects.get(id=member)
        gender = request.POST.get('gender')
        reference = request.POST.get('reference')
        data = Subscription(
            user=user1,
            trainer=trainer1,
            course=course,
            gender=gender,
            price_total=price_plan,
            refrence=reference,
            payment_status='Pending',  # Set the initial payment status as 'Pending' or customize as needed
            status='subscription Confirmed',  # Set the initial status as 'subscription Confirmed' or customize as needed
            is_subscribed=False,  # Set the initial value for 'is_subscribed' as False or customize as needed
            subscription_number='',  # This will be generated later
            DueDate=None,  # Set the initial DueDate as None or customize as needed
        )
        data.save()
        
        # Generate order number
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        subscription_number = current_date + str(data.id)
        data.subscription_number = subscription_number
        data.save()
        context={
            'username' :user1.username,
            'course_purchased': course,
            'trainer':trainer1,
            'price_plan':price_plan.price,
            'subscription_number': subscription_number

        }
        
        
        return render(request,'payment.html',context)
    return render(request,'enrollment.html')

def payments(request):
    body = json.loads(request.body)
    
    try:
        client = Subscription.objects.get(
            user=request.user,
            is_subscribed=False,
            subscription_number=body['orderID'],
            price_total=None
        )
    except Subscription.DoesNotExist:
        return JsonResponse({'message': 'Subscription not found.'}, status=404)

    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        order_id=client.subscription_number,
        payment_method=body['payment_method'],
        amount_paid=client.price_total,
        status='True'
    )
    payment.save()

    # Update the subscription with the payment details
    client.payment = payment
    client.is_subscribed = True
    client.save()

    # Send the response back to the client
    data = {
        'order_number': client.subscription_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

def workout_plan(request):

    return render (request,'workoutplan.html')

def search(request):
    
    course = None
       
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        
        print(keyword)
        if keyword:
            course = Course.objects.filter(
                Q(description__icontains=keyword) | Q(course_name__icontains=keyword))
        else:
           return redirect('course')
    
    print(course)
            
    context = {
        'course': course
    }
    return render(request,'course.html',context)



def order_complete(request):
    subscription_number = request.GET.get('subscription_number')
    transID = request.GET.get('payment_id')
    try:
        subscription = Subscription.objects.get(subscription_number=subscription_number)
        total = subscription.price_total

        
        grand_total = total
        payment = Payment.objects.get(payment_id=transID)

        context = {
            'subscription_number': subscription_number,
            'transID': payment.payment_id,
            'payment': payment,
            'grand_total': grand_total

        }

        return render(request, 'order_complete.html', context)
    except Exception as e:
        print(e)
        return redirect('home')



def cash_on_delivery(request, id):
    user1=request.user
    
        
    subs = Subscription.objects.get( subscription_number =id)
    price=subs.price_total.price
    
    # print(subs.subscription_number)
    # print(user1)
    # payment = Payment.objects.create(
    #     user=user1,
    #     payment_id='12234',
    #     order_id=subs.subscription_number,
    #     payment_method='Pay in counter',
    #     amount_paid=price,
    #     status='False'
    # )
    # print('hai')
    # payment.save()
    # subs.payment = payment
    # subs.is_subscribed = True
    # subs.save()
    
    

    subscriber = Subscription.objects.filter(subscription_number=id)
    context = {
        'user':user1,
        'subscription_number': subs.subscription_number,
        'price' : price
        


    }
    
    return render(request, 'COD_success.html',context)
    
    


@login_required(login_url='user_login')
def user_profile(request):
    user = request.user
    try:
        profile = userProfile.objects.get(user=user)
    except userProfile.DoesNotExist:
        # Handle the case where the userProfile does not exist
        profile = None
    
    context = {
        'user': user,
        'profile': profile
    }   
    
    return render(request, 'user_profile.html', context)

def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm()
    
    return render(request, 'create_user_profile.html', {'form': form})




def gallery(request):

    return render(request,'gallery.html')

def about_us(request):

    return render(request,'about-us.html')



