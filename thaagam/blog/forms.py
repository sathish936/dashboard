

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StaffProfile
from .models import Task

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        help_text=''  # removes default help text
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        help_text=''  # removes default help text
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        help_text=''  # removes default help text
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
        }
        help_texts = {
            'username': '',  # removes default username help text
        }




class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['user', 'age', 'contact', 'achievements', 'department']




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['staff','title', 'description', 'is_completed'] 


class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    is_staff = forms.BooleanField(required=False, label="Staff Access")
    is_superuser = forms.BooleanField(required=False, label="Superuser Access")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'is_staff', 'is_superuser']
        help_texts = {
            'username': None,
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')
        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data