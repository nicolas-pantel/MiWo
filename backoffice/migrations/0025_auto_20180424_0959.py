# Generated by Django 2.0.2 on 2018-04-24 09:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0024_auto_20180424_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_from',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='From'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_to',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 1, 9, 59, 27, 634444, tzinfo=utc), verbose_name='To'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 1, 9, 59, 27, 635878, tzinfo=utc), verbose_name='Expiration date'),
        ),
    ]
