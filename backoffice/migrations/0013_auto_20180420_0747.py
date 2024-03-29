# Generated by Django 2.0.2 on 2018-04-20 07:47

import cloudinary.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0012_auto_20180419_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='publication',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 27, 7, 47, 50, 337844, tzinfo=utc), verbose_name='Expiration date'),
        ),
        migrations.AddField(
            model_name='publication',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='publication',
            name='pub_type',
            field=models.CharField(choices=[('video', 'Video')], default='video', max_length=50, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='publication',
            name='social_network',
            field=models.CharField(choices=[('youtube', 'Youtube')], default='youtube', max_length=150, verbose_name='Social network'),
        ),
    ]
