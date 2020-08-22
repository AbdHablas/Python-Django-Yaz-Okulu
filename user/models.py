from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.forms import ModelForm
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=200)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    avatar = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_profile(self):
        return ' [ ' + self.user.username + ' ] ' + self.user.first_name + ' ' + self.user.last_name

    def avatar_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.avatar.url))

    avatar_tag.short_description = 'Avatar'


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'avatar']
