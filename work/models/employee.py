##
#     Project: Django Milazzo Inn
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import collections
import csv
import datetime
import io
import os.path

from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import path
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

import codicefiscale

import work.models

from locations.models import Country, Location

from utility.admin import AdminTextInputFilter
from utility.admin_actions import ExportCSVMixin
from utility.admin_widgets import AdminImageWidget_128x128
from utility.forms import CSVImportForm
from utility.misc import reverse_with_query


class Employee(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=10,
                           default='unknown',
                           choices=(('male', 'Male'),
                                    ('female', 'Female'),
                                    ('unknown', 'Unknown')))
    birth_date = models.DateField()
    birth_location = models.ForeignKey('locations.Location',
                                       on_delete=models.PROTECT,
                                       default=0,
                                       related_name='employee_birth_location')
    address = models.TextField(blank=True)
    location = models.ForeignKey('locations.Location',
                                 on_delete=models.PROTECT,
                                 default=0,
                                 related_name='employee_location')
    postal_code = models.CharField(max_length=15, blank=True)
    phone1 = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    vat_number = models.CharField(max_length=255, blank=True)
    tax_code = models.CharField(max_length=255)
    bank_account = models.CharField(max_length=255, blank=True)
    permit = models.CharField(max_length=255, blank=True)
    permit_location = models.ForeignKey('locations.Location',
                                        on_delete=models.PROTECT,
                                        default=0,
                                        blank=True,
                                        null=True)
    permit_date = models.DateField(blank=True, null=True, default=None)
    permit_expiration = models.DateField(blank=True, null=True, default=None)
    photo = models.ImageField(null=True, blank=True,
                              upload_to='hotels/images/employees/',
                              default='standard:genre_unknown_1')

    class Meta:
        # Define the database table
        db_table = 'work_employees'
        ordering = ['first_name', 'last_name']
        unique_together = ('first_name', 'last_name', 'tax_code')

    def __str__(self):
        return '{FIRST_NAME} {LAST_NAME}'.format(
            FIRST_NAME=self.first_name,
            LAST_NAME=self.last_name)

    def clean(self):
        """Validate model fields"""
        # Check tax code field
        tax_code = self.tax_code.upper().strip().ljust(16)
        if not codicefiscale.isvalid(tax_code):
            # Invalid tax code
            raise ValidationError({'tax_code': _('Invalid Tax Code')})
        elif codicefiscale.control_code(tax_code[:15]) != tax_code[15]:
            # Unmatching check digit
            raise ValidationError({'tax_code': _('Incorrect Tax Code')})
        elif Employee.objects.filter(tax_code=tax_code).exclude(
                pk=self.id):
            # Existing tax code
            raise ValidationError({'tax_code': _('Existing Tax Code')})
        else:
            # No errors
            self.tax_code = tax_code

    def get_active_contract_query(self, employee_ref):
        return work.models.Contract.objects.filter(
            # Current employee
            models.Q(employee=employee_ref),
            # Status enabled
            models.Q(status=True),
            # Start date less or equal than today
            models.Q(start_date__lte=datetime.date.today()),
            # End date is missing or after or equal today
            (models.Q(end_date__isnull=True) |
             models.Q(end_date__gt=datetime.date.today())
            ))

    def get_active_contract(self):
        contracts = self.get_active_contract_query(self)
        return contracts[0] if contracts else None


class EmployeeFirstNameInputFilter(AdminTextInputFilter):
    parameter_name = 'first_name'
    title = 'first name'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(first_name__icontains=self.value())


class EmployeeLastNameInputFilter(AdminTextInputFilter):
    parameter_name = 'last_name'
    title = 'last name'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(last_name__icontains=self.value())


class EmployeeTaxCodeInputFilter(AdminTextInputFilter):
    parameter_name = 'tax_code'
    title = 'tax code'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tax_code__icontains=self.value())


class EmployeeBirthLocationCountryFilter(admin.SimpleListFilter):
    parameter_name = 'birth_location'
    title = 'Birth Location'

    def lookups(self, request, model_admin):
        return Country.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(birth_location__region__country=self.value())



class EmployeeAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('id', 'first_name', 'last_name', 'tax_code',
                    'country', 'photo_thumbnail', 'active_contract')
    list_display_links = ('id', 'first_name', 'last_name', 'tax_code')
    list_filter = (EmployeeFirstNameInputFilter,
                   EmployeeLastNameInputFilter,
                   EmployeeTaxCodeInputFilter,
                   EmployeeBirthLocationCountryFilter)
    change_list_template = 'utility/import_csv/change_list.html'
    readonly_fields = ('id', 'standard_photos')
    radio_fields = {'genre': admin.HORIZONTAL}
    actions = ('action_export_csv', )
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'FIRST NAME': 'first_name',
        'LAST NAME': 'last_name',
        'DESCRIPTION': 'description',
        'GENRE': 'genre',
        'BIRTH DATE': 'birth_date',
        'BIRTH LOCATION': 'birth_location',
        'ADDRESS': 'address',
        'LOCATION': 'location',
        'POSTAL CODE': 'postal_code',
        'PHONE1': 'phone1',
        'PHONE2': 'phone2',
        'EMAIL': 'email',
        'VAT NUMBER': 'vat_number',
        'TAX CODE': 'tax_code',
        'PERMIT': 'permit',
        'PERMIT LOCATION': 'permit_location',
        'PERMIT DATE': 'permit_date',
        'PERMIT EXPIRATION': 'permit_expiration',
    })

    def save_model(self, request, obj, form, change):
        if not obj.photo or str(obj.photo).startswith('standard:'):
            iconset = 'standard:{ICONSET}'
            obj.photo = iconset.format(ICONSET=request.POST['standard_image'])
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Add subquery for active contract
        contracts = self.model.get_active_contract_query(None,
                                                         models.OuterRef('pk'))
        # Add annotated fields for contract id and company
        queryset = queryset.annotate(
            _country=models.F('birth_location__region__country'),
            _contract_id=models.Subquery(contracts.values('pk')[:1]),
            _contract_company=models.Subquery(
                contracts.values('company__name')[:1]),
        )
        return queryset

    def get_urls(self):
        urls = [
            path('import/', self.import_csv),
        ] + super().get_urls()
        return urls

    def import_csv(self, request):
        def append_error(type_name, item):
            """Append an error message to the messages list"""
            error_message = 'Unexpected {TYPE} "{ITEM}"'.format(TYPE=type_name,
                                                                ITEM=item)
            if error_message not in error_messages:
                error_messages.append(error_message)
                self.message_user(request, error_message, messages.ERROR)

        if request.method == 'POST':
            # Preload locations
            locations = {}
            for item in Location.objects.all():
                locations[str(item)] = item
            # Load CSV file content
            csv_file = io.TextIOWrapper(
                request.FILES['csv_file'].file,
                encoding=request.POST['encoding'])
            reader = csv.DictReader(
                csv_file,
                delimiter=request.POST['delimiter'])
            # Load data from CSV
            error_messages = []
            employees = []
            for row in reader:
                if row['BIRTH LOCATION'] not in locations:
                    append_error('location', row['BIRTH LOCATION'])
                if row['LOCATION'] not in locations:
                    append_error('location', row['LOCATION'])
                if row['PERMIT LOCATION'] not in locations:
                    append_error('location', row['PERMIT LOCATION'])
                # If no error create a new Room object
                employees.append(Employee(first_name=row['FIRST NAME'],
                                          last_name=row['LAST NAME'],
                                          description=row['DESCRIPTION'],
                                          genre=row['GENRE'],
                                          birth_date=row['BIRTH DATE']
                                                     if row['BIRTH DATE']
                                                     else None,
                                          birth_location=locations[
                                              row['BIRTH LOCATION']],
                                          address=row['ADDRESS'],
                                          location=locations[row['LOCATION']],
                                          postal_code=row['POSTAL CODE'],
                                          phone1=row['PHONE1'],
                                          phone2=row['PHONE2'],
                                          email=row['EMAIL'],
                                          vat_number=row['VAT NUMBER'],
                                          tax_code=row['TAX CODE'],
                                          permit=row['PERMIT'],
                                          permit_location=locations[
                                              row['PERMIT LOCATION']],
                                          permit_date=row['PERMIT DATE']
                                                      if row['PERMIT DATE']
                                                      else None,
                                          permit_expiration=
                                              row['PERMIT EXPIRATION']
                                              if row['PERMIT EXPIRATION']
                                              else None,
                                         ))
            # Save data only if there were not errors
            if not error_messages:
                Employee.objects.bulk_create(employees)
                self.message_user(request, 'Your CSV file has been imported')
            return redirect('..')
        return render(request,
                      'utility/import_csv/form.html',
                      {'form': CSVImportForm()})

    def detail_photo_image(self, instance, width, height):
        if instance.photo.url.startswith(
                os.path.join(settings.MEDIA_URL, 'standard%3A')):
            iconset = instance.photo.url.split('%3A', 1)[1]
            base_url = os.path.join(settings.STATIC_URL,
                                    'hotels/images/{ICONSET}/'
                                    '{SIZE}x{SIZE}.png')
            url_thumbnail = base_url.format(ICONSET=iconset, SIZE=width)
            url_image = base_url.format(ICONSET=iconset, SIZE=512)
        else:
            # Show image
            url_thumbnail = instance.photo.url
            url_image = url_thumbnail

        return mark_safe('<a href="{url}" target="_blank">'
                         '<img src="{thumbnail}" '
                         'width="{width}" '
                         'height={height} />'.format(url=url_image,
                                                     thumbnail=url_thumbnail,
                                                     width=width,
                                                     height=height))

    def photo_image(self, instance):
        return self.detail_photo_image(instance, 128, 128)

    def photo_thumbnail(self, instance):
        return self.detail_photo_image(instance, 48, 48)

    def formfield_for_dbfield(self, db_field, **kwargs):
        # For ImageField fields replace the rendering widget
        if isinstance(db_field, models.ImageField):
            kwargs['widget'] = AdminImageWidget_128x128
            # Remove request argument
            kwargs.pop('request', None)
            return db_field.formfield(**kwargs)
        else:
            return super().formfield_for_dbfield(db_field, **kwargs)

    def get_fields(self, request, obj=None):
        """Reorder the fields list"""
        fields = super().get_fields(request, obj)
        fields = ['id', ] + [k for k in fields if k not in ('id')]
        return fields

    def standard_photos(self, instance):
        template = loader.get_template('hotels/employee_standard_photos.html')
        context = {
            'photo': str(instance.photo).replace('standard:', ''),
            'iconsets': ('genre_unknown_1',
                         'genre_female_1',
                         'genre_female_2',
                         'genre_female_3',
                         'genre_female_4',
                         'genre_male_1',
                         'genre_male_2',
                         'genre_male_3',
                         'genre_male_4',
                         'genre_male_5',
                         'genre_male_6',
                         'genre_male_7')
        }
        return template.render(context)

    def active_contract(self, instance):
        if instance._contract_id:
            link = reverse_with_query(view='admin:work_contract_change',
                                      args=[instance._contract_id])
            link_classes = ''
            link_text = instance._contract_company
        else:
            link = reverse_with_query(view='admin:work_contract_add',
                                      query={'employee': instance.pk})
            link_classes = 'addlink'
            link_text = _('Add')
        return mark_safe('<a href="{LINK}" {CLASSES}>{TEXT}</a>'.format(
            LINK=link,
            CLASSES='class="{CLASSES}"'.format(CLASSES=link_classes)
                    if link_classes else '',
            TEXT=link_text))

    def country(self, instance):
        return instance._country
