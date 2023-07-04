from django import forms
from trainer.models import Trainer

class RegistrationForm(forms.ModelForm):
    

    class Meta:
        model=Trainer
        fields=['username','email','phone','password','specialized_course','age','gender','certificates','profile_pictures']

    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

# class ProfileForm(forms.ModelForm):
    

#     class Meta:
#         model=TrainerProfile
#         fields=['user','specialized_course','bio','experience','profile_picture','height','weight','address']

    
#     def __init__(self,*args,**kwargs):
#         super(ProfileForm,self).__init__(*args,**kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
#         self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})



