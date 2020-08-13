# Register your models here.
from django.contrib import admin

from .models import Category, Car, Image


class CarImageInline(admin.TabularInline):
    model = Image
    extra = 8


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent', 'image']
    list_filter = ['status']



class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rent_price', 'description', 'passenger_amount',
                    'door_number', 'image_tag', 'Bag', 'transmission_type', 'miles', 'details', 'parent', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['category', 'status']
    inlines = [CarImageInline]


class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'Car', 'image_tag']
    readonly_fields = ('image_tag',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Image, ImageAdmin)
