# Generated by Django 2.1.3 on 2018-12-03 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_auto_20181203_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='permit_location',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Location'),
        ),
    ]