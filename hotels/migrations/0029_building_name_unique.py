# Generated by Django 2.1.3 on 2018-12-01 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0028_employee_photo'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='building',
            unique_together={('name',)},
        ),
    ]