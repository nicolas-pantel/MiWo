# Generated by Django 2.0.2 on 2018-04-16 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0005_product_productimage'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('user', 'name')},
        ),
    ]