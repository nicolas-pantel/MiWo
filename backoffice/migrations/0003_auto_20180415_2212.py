# Generated by Django 2.0.2 on 2018-04-15 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0002_campaign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Name'),
        ),
    ]
