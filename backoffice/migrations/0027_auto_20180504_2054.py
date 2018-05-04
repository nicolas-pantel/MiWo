# Generated by Django 2.0.2 on 2018-05-04 20:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0026_auto_20180427_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='video_id',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Video ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_to',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 11, 20, 54, 27, 143130, tzinfo=utc), verbose_name='To'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 11, 20, 54, 27, 144725, tzinfo=utc), verbose_name='Expiration date'),
        ),
    ]
