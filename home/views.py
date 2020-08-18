from unicodedata import category

from django.core.checks import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import Car, Category
from home.models import Setting, ContactMessage, ContactForm


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:1]
    categories = Category.objects.all()
    cars = Car.objects.all()
    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderdata, 'categories': categories, 'cars': cars}
    return render(request, 'index.html', context)


def ListCar(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:1]
    categories = Category.objects.all()
    cars = Car.objects.all()
    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderdata, 'categories': categories, 'cars': cars}
    return render(request, 'ListCar.html', context)


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
