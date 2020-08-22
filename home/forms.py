from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from user.models import UserProfile


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
