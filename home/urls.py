from django.urls import path
from home import views


urlpatterns = [
    path('',views.index,name='home'),
    path('about_us/',views.about_us,name='about_us'),
    path('user-profile/',views.user_profile,name='user_profile'),
    path('enrollment/<int:id>/',views.enrollment,name='enrollment'),
    
    
    
]
