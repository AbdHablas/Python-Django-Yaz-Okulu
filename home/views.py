from unicodedata import category

from django.contrib.auth import logout, authenticate, login
from django.core.checks import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import Car, Category
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactMessage, ContactForm
from home import views


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:1]
    categories = Category.objects.all()
    cars = Car.objects.all()
    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderdata, 'categories': categories, 'cars': cars}
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    categories = Category.objects.all()
    context = {'setting': setting, 'page': 'about', 'categories': categories}
    return render(request, 'about.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    categories = Category.objects.all()
    context = {'setting': setting, 'page': 'references', 'categories': categories}
    return render(request, 'references.html', context)


def contactus(request):
    setting = Setting.objects.get(pk=1)
    categories = Category.objects.all()
    context = {'setting': setting, 'page': 'contact', 'categories': categories}
    return render(request, 'contact.html', context)


def contact(request):
    setting = Setting.objects.get(pk=1)
    categories = Category.objects.all()
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            context = {'setting': setting, 'page': 'contact', 'categories': categories, 'messages': [
                {'success': "Your message has ben sent. Thank you for your message.", "tag": 'success'}]}
            return render(request, 'contact.html', context)
    context = {'setting': setting, 'page': 'contact', 'categories': categories}
    return render(request, 'contact.html', context)


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        query = request.POST['Search']
        cars = Car.objects.all()
        cars = Car.objects.filter(title__icontains=query)  # SELECT * FROM product WHERE title LIKE '%query%'
        context = {'cars': cars, 'searchname': query}
        return render(request, 'search_car.html', context)
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:1]
    categories = Category.objects.all()
    cars = Car.objects.all()
    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderdata, 'categories': categories, 'cars': cars}
    return render(request, 'index.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            context = {'category': category, 'messages': [
                {'danger': "Login Error .. Try Again ..", "tag": 'danger'}]}
            return render(request, 'login.html', context)
    context = {'category': category}
    return render(request, 'login.html', context)


def signup_view(request):
    category = Category.objects.all()
    context = {'category': category}
    if request.method == 'POST':  # check post
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            return render(request, 'login.html', context)
        else:
            context = {'category': category, 'messages': [
                {'danger': str(form.errors), "tag": 'danger'}]}
    return render(request, 'signup.html', context)


def car_details(request):
    categories = Category.objects.all()
    car = Car.objects.filter(id__in=[request.GET.get('car_id', '')])[0]
    context = {'category': category, 'car': car}
    return render(request, 'car_details.html', context)


def ListCar(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:1]
    cars = Car.objects.all()
    categories = Category.objects.all()
    cat_id = request.GET.get('cat', '')
    if 'cat' not in request.GET:
        context = {'setting': setting, 'page': 'Home', 'sliderdata': sliderdata, 'categories': categories, 'cars': cars}
        return render(request, 'ListCar.html', context)
    sub_categories = Category.objects.extra(where=["parent_id='" + cat_id + "'"]).values_list('id', flat=True)
    cat_ids = []
    for sub_category in sub_categories:
        cat_ids.append(sub_category)
    cat_ids.append(cat_id)
    cars = Car.objects.filter(category_id__in=cat_ids)
    context = {'setting': setting, 'page': 'Home', 'sliderdata': sliderdata, 'categories': categories, 'cars': cars}
    return render(request, 'ListCar.html', context)
    # return HttpResponseRedirect('/listCar')
