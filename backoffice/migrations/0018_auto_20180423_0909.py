# Generated by Django 2.0.2 on 2018-04-23 09:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0017_auto_20180423_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 30, 9, 9, 37, 553653, tzinfo=utc), verbose_name='Expiration date'),
        ),
    ]
