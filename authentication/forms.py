from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    

    class Meta:
        model=CustomUser
        fields=['username','email','phone','password']

    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

   



class UserForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields =    ('username','phone')
