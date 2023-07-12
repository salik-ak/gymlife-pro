from django.urls import path
from home import views


urlpatterns = [
    path('',views.index,name='home'),
    path('about_us/',views.about_us,name='about_us'),
    path('user-profile/',views.user_profile,name='user_profile'),
    path('enrollment/<int:id>/',views.enrollment,name='enrollment'),
    path('gallery/',views.gallery,name='gallery'),
    path('payments/', views.payments, name='payments'),
    path('enrolled/', views.enrolled, name='enrolled'),
    path('order_complete/',views.order_complete, name='order_complete'),
    path('workout_plan/',views.workout_plan, name='workout_plan'),
    path('search/',views.search, name='search'),
    path('cash_on_delivery/<int:id>/',views.cash_on_delivery, name='cash_on_delivery'),
     path('create-profile/',views.create_user_profile, name='create_user_profile'),
    

    
    
    
]
