from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, Select, FileInput

from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='User Name :')
    email = forms.EmailField(max_length=200, label='Email :')
    first_name = forms.CharField(max_length=100, label='First Name :')
    last_name = forms.CharField(max_length=100, label='Last Name :')

    class Meta:
        model = User
        # fields = '__all__'
        fields = ('username', 'email', 'first_name', 'last_name')


