# Generated by Django 2.1.5 on 2019-01-16 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0022_employee_tax_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='bank_account',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
