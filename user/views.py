from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from car.models import Category
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
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


@login_required(login_url='/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        categories = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,   'categories': categories
                                                      })


def user_update(request):
    category = Category.objects.all()
    context = {
        'category': category,
    }
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(
    instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            current_user = request.user
            profile = UserProfile.objects.get(user_id=current_user.id)
            context = {
                'category': category,
                'message': 'Your account has been updated',
                'profile': profile
            }
            return render(request, 'user_profile.html', context)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
        instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'categories': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
    return render(request, 'user_update.html', context)
