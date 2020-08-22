from django.shortcuts import render
from car.models import Category
from user.models import UserProfile


def index(request):
    categories = Category.objects.all()

    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'categories': categories, 'profile': profile}
    return render(request, 'user_profile.html', context)


