from django.contrib import admin
from home.models import MembershipPlan,Payment,Subscription,WorkoutPlanExercise,WorkoutPlan,Exercise,userProfile

# Register your models here.
admin.site.register(MembershipPlan),
admin.site.register(Payment),
admin.site.register(Subscription),
admin.site.register(WorkoutPlanExercise),
admin.site.register(WorkoutPlan),
admin.site.register(Exercise)
admin.site.register(userProfile),
# Register your models here.
