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
import io

from django.db import models
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.html import mark_safe

from ..admin_actions import ExportCSVMixin
from ..admin_widgets import AdminImageWidget_128x128
from ..forms import CSVImportForm


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
    address = models.TextField(blank=True)
    phone1 = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    vat_number = models.CharField(max_length=255, blank=True)
    tax_code = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(null=True, blank=True,
                              upload_to='hotels/images/employees/')

    class Meta:
        # Define the database table
        db_table = 'hotels_employees'
        ordering = ['first_name', 'last_name']
        unique_together = ('first_name', 'last_name', 'tax_code')

    def __str__(self):
        return '{FIRST_NAME} {LAST_NAME}'.format(
            FIRST_NAME=self.first_name,
            LAST_NAME=self.last_name)


class EmployeeAdminInputFilter(admin.SimpleListFilter):
    template = 'hotels/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return (('', ''),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class FirstNameAdminNameFilter(EmployeeAdminInputFilter):
    parameter_name = 'first_name'
    title = 'first name'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(first_name__icontains=self.value())


class LastNameAdminNameFilter(EmployeeAdminInputFilter):
    parameter_name = 'last_name'
    title = 'last name'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(last_name__icontains=self.value())


class TaxCodeAdminNameFilter(EmployeeAdminInputFilter):
    parameter_name = 'tax_code'
    title = 'tax code'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tax_code__icontains=self.value())


class EmployeeAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('id', 'first_name', 'last_name', 'tax_code',
                    'photo_thumbnail')
    list_display_links = ('id', 'first_name', 'last_name', 'tax_code')
    list_filter = (FirstNameAdminNameFilter,
                   LastNameAdminNameFilter,
                   TaxCodeAdminNameFilter)
    change_list_template = 'hotels/change_list.html'
    readonly_fields = ('id', )
    actions = ('action_export_csv', )
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'FIRST NAME': 'first_name',
        'LAST NAME': 'last_name',
        'DESCRIPTION': 'description',
        'GENRE': 'genre',
        'BIRTH DATE': 'birth_date',
        'ADDRESS': 'address',
        'PHONE1': 'phone1',
        'PHONE2': 'phone2',
        'EMAIL': 'email',
        'VAT NUMBER': 'vat_number',
        'TAX CODE': 'tax_code',
    })

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
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
                # If no error create a new Room object
                employees.append(Employee(first_name=row['FIRST NAME'],
                                          last_name=row['LAST NAME'],
                                          description=row['DESCRIPTION'],
                                          genre=row['GENRE'],
                                          birth_date=row['BIRTH DATE'],
                                          address=row['ADDRESS'],
                                          phone1=row['PHONE1'],
                                          phone2=row['PHONE2'],
                                          email=row['EMAIL'],
                                          vat_number=row['VAT NUMBER'],
                                          tax_code=row['TAX CODE'],
                                         ))
            # Save data only if there were not errors
            if not error_messages:
                Employee.objects.bulk_create(employees)
                self.message_user(request, 'Your CSV file has been imported')
            return redirect('..')
        return render(request,
                      'hotels/form_csv_import.html',
                      {'form': CSVImportForm()})

    def detail_photo_image(self, instance, width, height):
        if instance.photo:
            return mark_safe('<img src="{url}" '
                             'width="{width}" '
                             'height={height} />'.format(
                url = instance.photo.url,
                width=width,
                height=height,
                ))
        else:
            return ''

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
            return super(self.__class__,self).formfield_for_dbfield(db_field,
                                                                    **kwargs)

    def get_fields(self, request, obj=None):
        """Reorder the fields list"""
        fields = super().get_fields(request, obj)
        fields = ['id', ] + [k for k in fields if k not in ('id')]
        return fields
