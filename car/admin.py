# Register your models here.
from django.contrib import admin

from .models import Category, Car, Image


class ProductImageInline(admin.TabularInline):
    model = Image
    extra = 8


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent']
    list_filter = ['status']


class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rent_price', 'description', 'passenger_amount',
                    'door_number', 'Bag', 'transmission_type', 'miles', 'details', 'parent', 'status']
    list_filter = ['category', 'status']
    inlines = [ProductImageInline]


class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'Car', 'image']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Image, ImageAdmin)
