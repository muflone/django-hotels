# Generated by Django 2.1.4 on 2018-12-30 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_header_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminsearchable',
            name='model',
            field=models.CharField(choices=[('BedTypeAdmin', 'BedTypeAdmin'), ('BrandAdmin', 'BrandAdmin'), ('BuildingAdmin', 'BuildingAdmin'), ('CompanyAdmin', 'CompanyAdmin'), ('ContinentAdmin', 'ContinentAdmin'), ('ContractAdmin', 'ContractAdmin'), ('ContractTypeAdmin', 'ContractTypeAdmin'), ('CountryAdmin', 'CountryAdmin'), ('EmployeeAdmin', 'EmployeeAdmin'), ('JobTypeAdmin', 'JobTypeAdmin'), ('LanguageAdmin', 'LanguageAdmin'), ('LocationAdmin', 'LocationAdmin'), ('LoginAdmin', 'LoginAdmin'), ('PositionAdmin', 'PositionAdmin'), ('RegionAdmin', 'RegionAdmin'), ('RegionAliasAdmin', 'RegionAliasAdmin'), ('RoomAdmin', 'RoomAdmin'), ('RoomTypeAdmin', 'RoomTypeAdmin'), ('StructureAdmin', 'StructureAdmin'), ('TabletAdmin', 'TabletAdmin'), ('TimestampAdmin', 'TimestampAdmin')], max_length=255),
        ),
        migrations.AlterField(
            model_name='adminsearchable',
            name='ref_model',
            field=models.CharField(choices=[('BedTypeAdmin', 'BedTypeAdmin'), ('BrandAdmin', 'BrandAdmin'), ('BuildingAdmin', 'BuildingAdmin'), ('CompanyAdmin', 'CompanyAdmin'), ('ContinentAdmin', 'ContinentAdmin'), ('ContractAdmin', 'ContractAdmin'), ('ContractTypeAdmin', 'ContractTypeAdmin'), ('CountryAdmin', 'CountryAdmin'), ('EmployeeAdmin', 'EmployeeAdmin'), ('JobTypeAdmin', 'JobTypeAdmin'), ('LanguageAdmin', 'LanguageAdmin'), ('LocationAdmin', 'LocationAdmin'), ('LoginAdmin', 'LoginAdmin'), ('PositionAdmin', 'PositionAdmin'), ('RegionAdmin', 'RegionAdmin'), ('RegionAliasAdmin', 'RegionAliasAdmin'), ('RoomAdmin', 'RoomAdmin'), ('RoomTypeAdmin', 'RoomTypeAdmin'), ('StructureAdmin', 'StructureAdmin'), ('TabletAdmin', 'TabletAdmin'), ('TimestampAdmin', 'TimestampAdmin')], max_length=255),
        ),
    ]
