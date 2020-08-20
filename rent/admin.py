from win10toast import ToastNotifier
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.html import format_html
from .models import Rent
from rent.task import send_rent_status_to_email


def approve_rent(modeladmin, request, queryset):
    queryset.update(approved=True)
    car = queryset[0].car
    car.available = False
    car.save()
    approve_rent.short_description = 'Approve rent'


def finish_rent(modeladmin, request, queryset):
    rent_end_date = parse_datetime(queryset[0].end_date)
    is_paid = queryset[0].paid
    now = timezone.now()
    if is_paid and now >= rent_end_date:
        queryset.update(finished=True)
        car = queryset[0].car
        car.available = True
        car.save()
        pk = queryset[0].pk
        send_rent_status_to_email.delay(pk, status='finished')
    else:
        toaster = ToastNotifier()
        toaster.show_toast('Error Notification!', "You can't finish this Rent yet.", duration=3)
    finish_rent.short_description = 'Finish rent'


@admin.register(Rent)
class RentModelAdmin(admin.ModelAdmin):
    def send_pdf_rent_detail_to_email(self, rent):
        return format_html('<a href="{}" onclick="return confirm(\'Are you sure?\')">Send Email</a>',
                           reverse('rent:send_pdf_to_email', kwargs={'pk': rent.pk}))

    send_pdf_rent_detail_to_email.short_description = 'Send PDF Rent detail to email'

    list_display = ('start_date', 'end_date', 'user', 'car', 'approved', 'canceled',
                    'finished', 'paid', 'rate', 'send_pdf_rent_detail_to_email')
    search_fields = ('user__username', 'car__model__name', 'car__name')
    list_filter = ('start_date', 'end_date')

    list_editable = ('approved', 'canceled', 'finished', 'paid')
    actions = (approve_rent, finish_rent)
