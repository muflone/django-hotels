# Generated by Django 2.1.4 on 2019-01-09 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0020_activityroom_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityroom',
            name='service_qty',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
