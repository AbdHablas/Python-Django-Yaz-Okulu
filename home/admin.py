from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactMessage, UserProfile


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'update_at', 'status']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'phone', 'address', 'city', 'country', 'image_tag']


admin.site.register(ContactMessage, ContactFormMessageAdmin)
admin.site.register(Setting)
admin.site.register(UserProfile, UserProfileAdmin)
