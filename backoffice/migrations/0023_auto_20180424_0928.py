# Generated by Django 2.0.2 on 2018-04-24 09:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0022_auto_20180424_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('entertainment', 'Entertainment'), ('sport', 'Sport'), ('culture', 'Culture')], default='entertainment', max_length=100, verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='date_from',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='From'),
        ),
        migrations.AddField(
            model_name='product',
            name='date_to',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 1, 9, 28, 37, 36281, tzinfo=utc), verbose_name='To'),
        ),
        migrations.AddField(
            model_name='product',
            name='legend',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Legend'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.CharField(choices=[('fashion', 'Fashion'), ('makeup', 'Makeup')], default='fashion', max_length=100, verbose_name='Subcategory'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 1, 9, 28, 37, 37773, tzinfo=utc), verbose_name='Expiration date'),
        ),
    ]
