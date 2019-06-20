# Generated by Django 2.1.5 on 2019-06-15 17:42

# noinspection PyPackageRequirements
import colorful.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0058_service_show_in_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='backcolor',
            field=colorful.fields.RGBColorField(default='#FFFFFF'),
        ),
        migrations.AddField(
            model_name='service',
            name='forecolor',
            field=colorful.fields.RGBColorField(default='#000000'),
        ),
    ]
