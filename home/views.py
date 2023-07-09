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
    
    if request.method == "POST":
        course = Course.objects.get(id=course_purchased.id)
        member = request.POST.get('member')
        price_plan = MembershipPlan.objects.get(id=member)
        gender = request.POST.get('gender')
        print(gender)
        reference = request.POST.get('reference')
        print(reference)
        data = Subscription(
            user=user,
            trainer=trainer,
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
            'username' :user2.username,
            'course_purchased':course_purchased,
            'trainer':trainer,
            'price_plan':price_plan.price

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

def gallery(request):

    return render(request,'gallery.html')

def about_us(request):

    return render(request,'about-us.html')



