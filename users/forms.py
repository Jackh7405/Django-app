from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class UserRegisterForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(
        label='Email address', 
        help_text='Your email address.'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class StudentUpdateForm(forms.ModelForm):
    """Form for updating student profile information"""
    
    class Meta:
        model = Student
        fields = ['photo', 'date_of_birth', 'address', 'city', 'country', 'course']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }