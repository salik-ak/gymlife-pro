from django.urls import path
from .import views

urlpatterns = [
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('', views.adminhome, name='adminhome'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('admin-userlist/', views.admin_userlist, name='admin_userlist'),
    path('<int:id>/blockuser/', views.blockuser, name='blockuser'),
    path('<int:id>/delete-user/',views.delete_user,name='delete_user'),
    path('admin_course_list/', views.admincourse, name='admin_course_list'),
    path('admin-add-course/', views.admin_add_course, name='admin_add_course'),
    path('<int:id>/update-course/', views.update_course,name='update_course'),
    path('admin_trainers_list/', views.admin_trainers_list, name='admin_trainers_list'),
    path('admin_subscription_list/', views.subscription_list, name='subscription_list'),
    path('<int:id>/block-course/', views.block_course, name='block_course'),
    path('<int:id>/delete-course/',views.delete_course,name='delete_course'),
    path('<int:id>/block-trainer/', views.block_trainer, name='block_trainer'),
    path('<int:id>/delete-trainer/',views.delete_trainer,name='delete_trainer'),
    path('<int:id>/delete-subscription/',views.delete_subscription,name='delete_subscription'),
    path('<int:id>/block-subscription/', views.block_subscription, name='block_subscription'),
    
]