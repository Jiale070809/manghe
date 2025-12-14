from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'height', 'body_type', 'interests']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['gender', 'height', 'body_type', 'interests', 'profile_image', 'privacy']
        widgets = {
            'interests': forms.TextInput(attrs={'placeholder': '用逗号分隔兴趣标签,如:电影,运动'}),
        }