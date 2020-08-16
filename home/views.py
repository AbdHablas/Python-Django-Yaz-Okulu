from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting


def index(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'home'}
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'about'}
    return render(request, 'about.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'references'}
    return render(request, 'references.html', context)
