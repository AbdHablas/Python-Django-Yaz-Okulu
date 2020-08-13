from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class Category(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=255, choices=STATUS)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




class Car(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # many to one relationship with category
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    passenger_amount = models.CharField(max_length=255, null=True, blank=True)
    door_number = models.CharField(max_length=255, null=True, blank=True)
    Bag = models.CharField(max_length=10, choices=STATUS, null=True, blank=True)
    transmission_type = models.CharField(max_length=255, null=True, blank=True)
    miles = models.CharField(max_length=255, null=True, blank=True)
    rent_price = models.IntegerField()
    details = models.TextField()
    status = models.CharField(max_length=255, choices=STATUS)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


class Image(models.Model):
    Car = models.ForeignKey(Car, related_name="Images", on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
