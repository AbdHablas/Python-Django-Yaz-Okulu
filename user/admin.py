from django.contrib import admin

# Register your models here.
from user.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'phone', 'address', 'city', 'country', 'avatar_tag']
    readonly_fields = ('avatar_tag',)


admin.site.register(UserProfile, UserProfileAdmin)
