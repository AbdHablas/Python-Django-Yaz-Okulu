from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('references', views.references, name='references'),
    path('contact', views.contact, name='contact'),
    path('ListCar', views.ListCar, name='ListCar'),
    path('search_car', views.search, name='search'),
]
