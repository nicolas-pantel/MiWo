# Generated by Django 2.0.2 on 2018-04-18 08:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0007_productimage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Url')),
                ('user', models.ForeignKey(on_delete='models.CASCADE', related_name='publications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]