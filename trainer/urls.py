from django.urls import path
from trainer import views


urlpatterns = [
   
    path('trainer/',views.trainer,name='trainer'),
    path('trainer_login/', views.trainer_login, name='trainer_login'),
    path('trainer_signup/', views.trainer_signup, name='trainer_signup'),
    # path('trainer_profile/', views.trainer_profile, name='trainer_profile'),
    # path('update_trainer_profile/', views.update_trainer_profile, name='update_trainer_profile'),
    
]