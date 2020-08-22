from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from car.models import Category
from user.forms import SignUpForm
from user.models import UserProfile


@login_required(login_url='/login')  # Check login
def index(request):
    categories = Category.objects.all()

    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'categories': categories, 'profile': profile}
    return render(request, 'user_profile.html', context)


def login_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':  # check post
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            context = {'categories': categories, 'messages': [
                {'danger': "Login Error .. Try Again ..", "tag": 'danger'}]}
            return render(request, 'login.html', context)
    context = {'categories': categories}
    return render(request, 'login.html', context)


def signup_view(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    if request.method == 'POST':  # check post
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Create data in profile table for user
                current_user = request.user
                data = UserProfile()
                data.user_id = current_user.id
                data.avatar = "images/users/user.png"
                data.save()
                messages.success(request, 'Your account has been created!')
                return HttpResponseRedirect('/')
            return render(request, 'login.html', context)
        else:
            context = {'categories': categories, 'messages': [
                {'danger': str(form.errors), "tag": 'danger'}]}
    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


