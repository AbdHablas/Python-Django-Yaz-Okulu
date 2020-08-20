from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from celery import task
from django.template.loader import render_to_string
from weasyprint import HTML
from win10toast import ToastNotifier
from .models import Rent


@task
def send_rent_status_to_email(pk, status):
    try:
        rent = Rent.objects.get(pk=pk)
        subject = 'Rent-a-car Rent detail'
        toaster = ToastNotifier()
        if status == 'paid':
            message = f'Your Rent #{rent.pk} is successfully paid. Enjoy driving & good luck!'
            toaster.show_toast('Paid Rent Notification!',
                               f'You paid the Rent #{rent.pk}', duration=3)
        elif status == 'finished':
            message = f'Your Rent #{rent.pk} is finished. Thank you for using our Rent-a-car service!'
            toaster.show_toast('Finished Rent Notification!',
                               f'Your Rent #{rent.pk} is finished.', duration=3)
        else:
            message = f'Your Rent #{rent.pk} is canceled. Best regards from our team!'
            toaster.show_toast('Canceled Rent Notification!',
                               f'You have canceled the Rent #{rent.pk}', duration=3)

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [rent.user.email])
        email.send()
        return True
    except Exception as e:
        return str(e)


@task
def send_pdf_to_email(pk):
    try:
        rent = Rent.objects.get(pk=pk)
        html = render_to_string('rent/rent_detail_pdf.html', {'rent': rent})
        out = BytesIO()
        HTML(string=html).write_pdf(out)

        subject = 'Rent-a-car Rent detail'
        message = f'We approved your Rent #{rent.pk}. You can see Rent detail in PDF attachment. ' \
                  'Thank you for using our Rent-a-car service!'
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [rent.user.email])
        email.attach('Rent #{}_{}.pdf'.format(rent.pk, rent.car.name),
                     out.getvalue(), 'application/pdf')
        email.send()
        return True
    except Exception as e:
        return str(e)




