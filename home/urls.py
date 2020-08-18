from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('about.html', views.about, name='about'),
    path('references.html', views.references, name='references'),
    path('contact.html', views.contact, name='contact'),
    path('ListCar.html', views.ListCar, name='ListCar')
]


