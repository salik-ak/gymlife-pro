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



# def cash_on_delivery(request, id):
#     # Move cart item to ordered product table
#     try:

#         order = Subscription.objects.get(user=request.user, is_ordered=False, order_number=id)
      
        
#         payment = Payment(
#             user=request.user,
#             payment_id=order.order_number,
#             order_id=order.order_number,
#             payment_method='Cash on Delivery',
#             amount_paid=order.order_total,
#             status='False'
#         )
#         payment.save()
#         order.payment = payment
#         order.is_ordered = True
#         order.save()
        
#         for cart_item in cart_items:
#             order_product = OrderProduct()
#             order_product.order_id = order.id
#             order_product.payment = payment
#             order_product.user_id = request.user.id
#             order_product.product_id = cart_item.product_id
#             order_product.quantity = cart_item.quantity
#             order_product.product_price = cart_item.product.price
#             order_product.ordered = True
#             order_product.save()

#             cart_item = CartItem.objects.get(id=cart_item.id)
#             product_variation = cart_item.variations.all()
            
#             order_product = OrderProduct.objects.get(id=order_product.id)

#             order_product.variations.set(product_variation)

#             order_product.save()

#             # Reduce quantity of product
#             product = Product.objects.get(id=cart_item.product_id)
#             product.stock -= cart_item.quantity
#             product.save()

#             # # Reduce quantity of variation

#             print(cart_item.id)
#             print(type(cart_item.variations))
#             print(cart_item.variations.all())
#             test = cart_item.variations.all()[0]
#             print(test)
#             variation = Variations.objects.filter(
#                 id__in=cart_item.variations.all())
#             for var in variation:
#                 var.stock -= cart_item.quantity
#                 var.save()

#             # clear cart
            
#         CartItem.objects.filter(user=request.user).delete()

#         ordered_products = OrderProduct.objects.filter(order_id=order.id)
#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'payment': payment,
#             'total': total,
#             'tax': tax,
#             'shipping': shipping,


#         }
        
#         return render(request, 'cod_success.html', context)
    
#     except Exception as e:
#         return redirect('home')



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



