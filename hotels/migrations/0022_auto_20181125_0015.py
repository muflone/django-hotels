# Generated by Django 2.1.3 on 2018-11-24 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0021_remove_building_floors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='floor',
        ),
        migrations.DeleteModel(
            name='Floor',
        ),
    ]
