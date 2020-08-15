from django.http import HttpResponse
from django.shortcuts import render

from ckeditor_uploader.fields import RichTextUploadingField


# Create your views here.
def index(request):
    return HttpResponse("Car Page")
