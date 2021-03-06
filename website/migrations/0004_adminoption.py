# Generated by Django 2.1.3 on 2018-11-26 00:34

from django.db import migrations, models


def initialize_admin_option(apps, schema_editor):
    AdminOption = apps.get_model('website', 'AdminOption')
    option = AdminOption(name='building.location.searchable',
                         value='0',
                         description='Replaces the Building location field '
                                     'with a Select2 widget instead of a '
                                     'fixed SELECT widget.')
    option.save()

    option = AdminOption(name='hotel.location.searchable',
                         value='0',
                         description='Replaces the Hotel location field '
                                     'with a Select2 widget instead of a '
                                     'fixed SELECT widget.')
    option.save()

class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_adminsection'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminOption',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'website_admin_options',
                'ordering': ['name'],
            },
        ),
        migrations.RunPython(initialize_admin_option),
    ]
