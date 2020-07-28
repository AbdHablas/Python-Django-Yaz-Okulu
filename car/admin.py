# Register your models here.
from django.contrib import admin

from .models import Category, Car


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent']
    list_filter = ['status']


admin.site.register(Category, CategoryAdmin)


class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rent_price', 'description', 'passenger_amount',
                    'door_number', 'Bag', 'transmission_type', 'miles', 'details', 'parent', 'status']
    list_filter = ['category']


admin.site.register(Car, CarAdmin)
