# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from car.models import Category, Car, Image, Comment


class CarImageInline(admin.TabularInline):
    model = Image
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent', 'image']
    list_filter = ['status']


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_cars_count', 'related_cars_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ['title']}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative car count
        qs = Category.objects.add_related_count(
            qs,
            Car,
            'category',
            'cars_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Car,
                                                'category',
                                                'cars_count',
                                                cumulative=False)
        return qs

    def related_cars_count(self, instance):
        return instance.cars_count
        related_cars_count.short_description = 'Related products (for this specific category)'

    def related_cars_cumulative_count(self, instance):
        return instance.cars_cumulative_count

    related_cars_cumulative_count.short_description = 'Related cars (in tree)'


class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rent_price', 'description', 'passenger_amount',
                    'door_number', 'Bag', 'transmission_type', 'image_tag', 'miles', 'parent', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['category', 'status']
    inlines = [CarImageInline]
    prepopulated_fields = {'slug': ['title']}


class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'Car', 'image_tag']
    readonly_fields = ('image_tag',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'status', 'create_at']
    list_filter = ['status']
    readonly_fields = ('subject', 'comment', 'ip', 'user', 'product', 'rate', 'id')


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Car, CarAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
