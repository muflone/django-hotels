# Generated by Django 2.2.10 on 2020-03-01 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0039_login_default_structure'),
    ]

    operations = [
        migrations.RunSQL('DROP VIEW IF EXISTS work_activities_full_view'),
    ]
