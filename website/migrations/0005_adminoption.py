from django.db import migrations, models


def initialize_admin_option(apps, schema_editor):
    AdminOption = apps.get_model('website', 'AdminOption')
    option = AdminOption.objects.get(name='hotel.location.searchable')
    option.name = 'structure.location.searchable'
    option.save()

    option = AdminOption.objects.get(name='hotel.location.searchable')
    option.delete()

    option = AdminOption(name='employee.birth_location.searchable',
                         value='0',
                         description='Replaces the Employee birth location '
                                     'field with a Select2 widget instead of '
                                     'a fixed SELECT widget.')
    option.save()

    option = AdminOption(name='employee.permit_location.searchable',
                         value='0',
                         description='Replaces the Employee permit location '
                                     'field with a Select2 widget instead of '
                                     'a fixed SELECT widget.')
    option.save()

    option = AdminOption(name='employee.location.searchable',
                         value='0',
                         description='Replaces the Employee location '
                                     'field with a Select2 widget instead of '
                                     'a fixed SELECT widget.')
    option.save()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_adminoption'),
    ]

    operations = [
        migrations.RunPython(initialize_admin_option),
    ]
