from django import forms
from .models import userProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['full_name', 'age', 'profile_picture', 'height', 'weight', 'address']
