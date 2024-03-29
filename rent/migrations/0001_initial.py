# Generated by Django 3.1 on 2020-08-20 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car', '0011_auto_20200820_0438'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.CharField(max_length=20)),
                ('approved', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('total_price', models.FloatField(blank=True, null=True)),
                ('rate', models.IntegerField(default=0)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='car.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Rents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'rent',
            },
        ),
    ]
