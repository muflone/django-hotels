# Generated by Django 2.1.3 on 2018-11-24 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0023_bed_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='phone1',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
