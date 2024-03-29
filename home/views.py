from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

import rent
from car.models import Car, Category
from home.forms import SearchForm
from home.models import Setting, ContactMessage, ContactForm

from rent.models import Rent
from user.models import UserProfile


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
                {'message': "Your message has ben sent. Thank you for your message.", "tag": 'success'}]}
            return render(request, 'contact.html', context)

        else:
            context = {'setting': setting, 'page': 'contact', 'categories': categories, 'messages': [
                {'message': str(form.errors), "tag": 'danger'}]}
            return render(request, 'contact.html', context)
    context = {'setting': setting, 'page': 'contact', 'categories': categories}
    return render(request, 'contact.html', context)


def search(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:1]
    categories = Category.objects.all()
    cars = Car.objects.all()
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        query = request.POST['Search']
        cars = Car.objects.filter(title__icontains=query)  # SELECT * FROM product WHERE title LIKE '%query%'
        context = {'cars': cars, 'searchname': query}
        context = {'setting': setting, 'page': 'home', 'searchname': query, 'sliderdata': sliderdata,
                   'categories': categories, 'cars': cars}
        return render(request, 'search_car.html', context)
    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderdata, 'categories': categories, 'cars': cars}
    return render(request, 'index.html', context)


def car_details(request):
    categories = Category.objects.all()
    car = Car.objects.filter(id__in=[request.GET.get('car_id', '')])[0]
    context = {'categories': categories, 'car': car}
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


def rent_car(request):
    categories = Category.objects.all()
    car_id = request.GET.get('car_id', '')
    car = Car.objects.filter(id__in=[car_id])[0]
    OlodRentCar = None
    OlodRentCar = Rent.objects.filter(car_id__in=[car_id]).filter(finished__in=[0])
    context = {'categories': categories, 'car': car}
    if request.method == 'POST':  # check post
        if request.user.is_authenticated:
            if OlodRentCar:
                context = {'categories': categories, 'car': car, 'message':
                    {'message': 'this Car is pocked', "tag": 'danger'}}
                return render(request, 'car_details.html', context)

            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            user_id = request.user.id
            data = {'start_date': start_date, 'end_date': end_date, 'user_id': user_id, 'car_id': car_id, 'approved': 0,
                    'finish': 0, 'canceled': 0, 'paid': 0, 'total_price': car.rent_price, 'rate': 0}
            form = RentCarForm(data)
            if form.is_valid():
                data = Rent()
                data.start_date = start_date
                data.end_date = end_date
                data.user_id = user_id
                data.car_id = car_id
                data.approved = 0
                data.finish = 0
                data.canceled = 0
                data.paid = 0
                data.total_price = car.rent_price
                data.rate = 0
                data.save()  # save data to table
                context = {'categories': categories, 'car': car, 'message':
                    {'message': "Reservation Done.", "tag": 'success'}}
            else:
                context = {'categories': categories, 'car': car, 'message':
                    {'message': form.errors, "tag": 'danger'}}
        else:
            return HttpResponseRedirect('/login')
    return render(request, 'car_details.html', context)


class RentCarForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()


def user_orders(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    orders = Rent.objects.filter(user_id=current_user.id)
    categories = Category.objects.all()
    cars = Car.objects.all()

    profile = UserProfile.objects.get(user_id=current_user.id)

    total = 0
    for el in orders:
        delta = el.end_date - el.start_date
        total = total + (el.total_price*delta.days)
    context = {'setting': setting, 'profile': profile, 'page': 'home', 'categories': categories, 'cars': cars, 'total': total,'orders': orders}
    return render(request, 'user_orders.html', context)


def cancel_rent(request):
    rent_id = request.GET.get('id', '')
    ActionRent = Rent.objec ,ts.get(id=rent_id)
    ActionRent.delete()
    category = Category.objects.all()
    current_user = request.user
    orders = Rent.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    total = 0
    for el in orders:
        delta = el.end_date - el.start_date
        total = total + (el.total_price * delta.days)
    context = {'rent': rent,
               'messages': 'Rent Deleted Successfully',
               'tag': 'success',
               'profile': profile,
               'category': category,
               'total': total,
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)
