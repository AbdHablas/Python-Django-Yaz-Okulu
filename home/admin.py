from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactMessage


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'update_at', 'status']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']


admin.site.register(ContactMessage, ContactFormMessageAdmin)
admin.site.register(Setting)
