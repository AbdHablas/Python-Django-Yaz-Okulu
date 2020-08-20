from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from RentalCar import settings
from car.models import Car


class Rent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Rents')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    approved = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    total_price = models.FloatField(null=True, blank=True)
    rate = models.IntegerField(default=0)

    class Meta:
        db_table = 'rent'


def __str__(self):
    status = 'Pending'
    if not self.approved and not self.paid and not self.finished and self.canceled:
        status = 'Canceled'
    elif (self.approved and not self.paid and not self.finished and not self.canceled) or \
            (self.approved and self.paid and not self.finished and not self.canceled):
        status = 'Active'
    elif self.approved and self.paid and self.finished and not self.canceled:
        status = 'Finished'
    return f'{self.user} rent a {self.car}, {self.start_date} - {self.end_date}, {status}'
