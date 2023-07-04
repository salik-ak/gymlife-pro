from django.urls import path
from course import views


urlpatterns = [
   
    path('course/',views.course,name='course'),
    path('course_details/<int:id>/',views.course_details,name='course_details'),
    
]



