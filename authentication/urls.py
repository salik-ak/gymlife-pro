from django.urls import path
from authentication import views


urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('activate/<uidb64>/<token>/',views.activate,name="activate"),
    
    

    
]   