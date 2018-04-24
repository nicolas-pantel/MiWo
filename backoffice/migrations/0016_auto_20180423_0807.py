# Generated by Django 2.0.2 on 2018-04-23 08:07

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0015_auto_20180423_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Number')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='backoffice.Profile')),
            ],
        ),
        migrations.AlterField(
            model_name='publication',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 30, 8, 7, 51, 68057, tzinfo=utc), verbose_name='Expiration date'),
        ),
    ]