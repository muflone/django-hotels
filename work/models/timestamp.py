##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2020 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import collections
import csv
import datetime
import io
import locale
import sys

from django.db import models
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import pgettext_lazy

from .contract import Contract
from .timestamp_direction import TimestampDirection

from utility.admin_widgets import AdminTimeWidget
from utility.forms import CSVImportForm
from utility.misc import (get_admin_options,
                          xhtml2pdf_render_from_template_response)
from utility.models import BaseModel, BaseModelAdmin


class Timestamp(BaseModel):
    contract = models.ForeignKey('Contract',
                                 on_delete=models.PROTECT,
                                 verbose_name=pgettext_lazy('Timestamp',
                                                            'contract'))
    structure = models.ForeignKey('hotels.Structure',
                                  default=0,
                                  on_delete=models.PROTECT,
                                  verbose_name=pgettext_lazy('Timestamp',
                                                             'structure'))
    direction = models.ForeignKey('TimestampDirection',
                                  on_delete=models.PROTECT,
                                  verbose_name=pgettext_lazy('Timestamp',
                                                             'direction'))
    date = models.DateField(verbose_name=pgettext_lazy('Timestamp',
                                                       'date'))
    time = models.TimeField(verbose_name=pgettext_lazy('Timestamp',
                                                       'time'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Timestamp',
                                                              'description'))

    class Meta:
        # Define the database table
        db_table = 'work_timestamps'
        ordering = ['contract', 'date', 'time']
        unique_together = ('contract', 'structure', 'direction',
                           'date', 'time')
        verbose_name = pgettext_lazy('Timestamp', 'Timestamp')
        verbose_name_plural = pgettext_lazy('Timestamp', 'Timestamps')

    def __str__(self):
        return '{CONTRACT} {STRUCTURE} {DIRECTION} {DATE} {TIME}'.format(
            CONTRACT=self.contract,
            STRUCTURE=self.structure,
            DIRECTION=self.direction,
            DATE=self.date,
            TIME=self.time)

    def employee(self):
        return self.contract.employee

    def roll_number(self):
        return self.contract.roll_number


class TimestampAdmin(BaseModelAdmin, AdminTimeWidget):
    change_list_template = 'utility/import_csv/change_list.html'
    date_hierarchy = 'date'
    list_select_related = ('contract', 'contract__employee')
    readonly_fields = ('id', )
    radio_fields = {'direction': admin.HORIZONTAL}
    actions = ('action_timestamps_hours_csv',
               'action_timestamps_hours_html',
               'action_timestamps_hours_pdf',
               'action_timestamps_days_csv',
               'action_timestamps_days_html',
               'action_timestamps_days_pdf')
    ordering = ['-date', '-time', 'contract']

    def first_name(self, instance):
        return instance.contract.employee.first_name
    first_name.short_description = pgettext_lazy('Employee', 'First name')

    def last_name(self, instance):
        return instance.contract.employee.last_name
    last_name.last_description = pgettext_lazy('Employee', 'Last name')

    def get_fields(self, request, obj=None):
        """Reorder the fields list"""
        fields = super().get_fields(request, obj)
        fields = ['id'] + [k for k in fields if k not in 'id']
        return fields

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
          'contract__employee', 'structure', 'structure__company', 'direction')

    def get_urls(self):
        urls = [
            path('import/', self.import_csv),
        ] + super().get_urls()
        return urls

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'contract':
            # Optimize value lookup for field employee
            kwargs['queryset'] = Contract.objects.all().select_related(
                'employee', 'company')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_timestamps_hours(self, request, queryset):
        queryset = queryset.order_by('date', 'contract', 'time')
        # Save TimestampDirection keys for enter and exit
        direction_enter = TimestampDirection.get_enter_direction().pk
        direction_exit = TimestampDirection.get_exit_direction().pk
        # Cycle each unique date/contract
        last_date = None
        last_contract_id = None
        results = []
        for timestamp in queryset:
            # Skip duplicated date/contract_id
            if (timestamp.date == last_date and
                    timestamp.contract_id == last_contract_id):
                continue
            # Save unique date/contract_id
            last_date = timestamp.date
            last_contract_id = timestamp.contract_id
            timestamp_export = TimestampHoursExport(timestamp)
            # Process only Enter/Exit timestamps
            for item in queryset.filter(date=last_date,
                                        contract_id=last_contract_id,
                                        direction__in=(direction_enter,
                                                       direction_exit)):
                if item.direction_id == direction_enter:
                    if timestamp_export.exit_time:
                        # Timestamp with a previous exit
                        results.append(timestamp_export.extract())
                        # Create new timestamp
                        timestamp_export = TimestampHoursExport(timestamp)
                    elif timestamp_export.enter_time:
                        # Timestamp with multiple enter
                        results.append(timestamp_export.extract())
                        # Create new timestamp
                        timestamp_export = TimestampHoursExport(timestamp)
                    timestamp_export.enter_time = item.time
                    timestamp_export.enter_description = item.description
                else:
                    if timestamp_export.exit_time:
                        # Timestamp with multiple exit
                        results.append(timestamp_export.extract())
                        # Create new timestamp
                        timestamp_export = TimestampHoursExport(timestamp)
                    timestamp_export.exit_time = item.time
                    timestamp_export.exit_description = item.description
            # Export timestamp only if valid
            if timestamp_export.is_valid():
                results.append(timestamp_export.extract())
            # Process only different timestamps
            for item in queryset.filter(date=last_date,
                                        contract_id=last_contract_id).exclude(
                                            direction__in=(direction_enter,
                                                           direction_exit)):
                timestamp_export = TimestampHoursExport(timestamp)
                timestamp_export.other_time = item.time
                timestamp_export.other_description = item.direction.description

                results.append(timestamp_export.extract())
        # Export data
        context = dict(
            # Include common variables for rendering the admin template
            self.admin_site.each_context(request),
            results=results
        )
        return context

    def action_timestamps_hours_csv(self, request, queryset):
        # Export data to CSV format
        context = self.get_timestamps_hours(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        return self.do_export_data_to_csv(
            data=context['results'],
            fields_map=TimestampHoursExport.fields_map,
            filename='timestamps_hours')
    action_timestamps_hours_csv.short_description = pgettext_lazy(
        'Timestamp',
        'Timestamps hours (CSV)')

    def action_timestamps_hours_html(self, request, queryset):
        context = self.get_timestamps_hours(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        # Split visible_columns in multiple values
        visible_columns = context['visible_columns']
        context['visible_columns'] = (
            [column.strip() for column in visible_columns.split(',')]
            if visible_columns else None)
        response = TemplateResponse(request,
                                    'work/timestamps_hours/admin.html',
                                    context)
        return response
    action_timestamps_hours_html.short_description = pgettext_lazy(
        'Timestamp',
        'Timestamps hours (HTML)')

    def action_timestamps_hours_pdf(self, request, queryset):
        context = self.get_timestamps_hours(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        # Split visible_columns in multiple values
        visible_columns = context['visible_columns']
        context['visible_columns'] = (
            [column.strip() for column in visible_columns.split(',')]
            if visible_columns else None)
        response = xhtml2pdf_render_from_template_response(
            response=TemplateResponse(request,
                                      'work/timestamps_hours/pdf.html',
                                      context),
            filename='')
        return response
    action_timestamps_hours_pdf.short_description = pgettext_lazy(
        'Timestamp',
        'Timestamps hours (PDF)')

    def get_timestamps_days(self, request, queryset):
        queryset = queryset.order_by('structure', 'contract', 'date', 'time')
        # Get minimum and maximum dates
        range_dates = queryset.aggregate(models.Min('date'),
                                         models.Max('date'))
        date_min = range_dates['date__min']
        date_max = range_dates['date__max']
        # Save TimestampDirection keys for enter and exit
        direction_enter = TimestampDirection.get_enter_direction()
        direction_exit = TimestampDirection.get_exit_direction()
        # Cycle each unique date/contract
        saved_contract_id = None
        results = []
        for timestamp in queryset:
            saved_date = None
            # Skip duplicated contract_id
            if timestamp.contract_id == saved_contract_id:
                continue
            # Save unique contract_id
            saved_contract_id = timestamp.contract_id
            timestamp_export = TimestampDaysExport(timestamp)
            for item in queryset.filter(contract_id=saved_contract_id):
                # Skip duplicated date
                if item.date == saved_date:
                    continue
                saved_date = item.date
                # Use enter short code for exit direction
                timestamp_direction = (
                    direction_enter
                    if item.direction_id == direction_exit.pk
                    else item.direction)
                timestamp_export.dates[item.date.toordinal()] = (
                    timestamp_direction.short_code)
            results.append(timestamp_export.extract(
                date_min=date_min,
                date_max=date_max,
                working_short_code=direction_enter.short_code))
        # Export data
        Direction = collections.namedtuple('Direction', 'short_code name')
        context = dict(
            # Include common variables for rendering the admin template
            self.admin_site.each_context(request),
            results=results,
            # Ordinals are the numeric days, used for keys
            ordinals=range(date_min.toordinal(), date_max.toordinal() + 1),
            # Dates are the date objects
            dates=[datetime.date.fromordinal(day)
                   for day
                   in range(date_min.toordinal(), date_max.toordinal() + 1)],
            # Directions for final report data
            directions=[Direction(item[0], item[1])
                        for item in (TimestampDirection.objects.exclude(
                            id__in=(0, direction_exit.pk)).order_by(
                            'name').values_list('short_code', 'name'))]
        )
        return context

    def action_timestamps_days_csv(self, request, queryset):
        # Export data to CSV format
        context = self.get_timestamps_days(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        return self.do_export_data_to_csv(
            data=context['results'],
            fields_map=dict(
                **TimestampDaysExport.fields_map,
                **dict([(datetime.date.fromordinal(day).strftime(
                        # Format dates headers
                        context.get('format_date', '%F')), day)
                        for day in context['ordinals']])),
            filename='timestamps_days')
    action_timestamps_days_csv.short_description = pgettext_lazy(
        'Timestamp',
        'Timestamps days (CSV)')

    def action_timestamps_days_html(self, request, queryset):
        context = self.get_timestamps_days(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        # Save locale and restore it after getting the days names
        old_locale = locale.getlocale(locale.LC_TIME)
        if context.get('locale'):
            # Format days headers
            locale.setlocale(locale.LC_TIME, context['locale'])
        context['days'] = [date.strftime('%a') for date in context['dates']]
        locale.setlocale(locale.LC_TIME, old_locale)
        # Split visible_columns in multiple values
        visible_columns = context['visible_columns']
        context['visible_columns'] = (
            [column.strip() for column in visible_columns.split(',')]
            if visible_columns else None)
        # Format dates
        if context.get('format_date'):
            context['dates'] = [date.strftime(context['format_date'])
                                for date in context['dates']]
        response = TemplateResponse(request,
                                    'work/timestamps_days/admin.html',
                                    context)
        return response
    action_timestamps_days_html.short_description = pgettext_lazy(
        'Timestamp',
        'Timestamps days (HTML)')

    def action_timestamps_days_pdf(self, request, queryset):
        context = self.get_timestamps_days(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        # Save locale and restore it after getting the days names
        old_locale = locale.getlocale(locale.LC_TIME)
        if context.get('locale'):
            # Format days headers
            locale.setlocale(locale.LC_TIME, context['locale'])
        context['days'] = [date.strftime('%a') for date in context['dates']]
        locale.setlocale(locale.LC_TIME, old_locale)
        # Split visible_columns in multiple values
        visible_columns = context['visible_columns']
        context['visible_columns'] = (
            [column.strip() for column in visible_columns.split(',')]
            if visible_columns else None)
        # Format dates
        if context.get('format_date'):
            context['dates'] = [date.strftime(context['format_date'])
                                for date in context['dates']]
        response = xhtml2pdf_render_from_template_response(
            response=TemplateResponse(request,
                                      'work/timestamps_days/pdf.html',
                                      context),
            filename='')
        return response
    action_timestamps_days_pdf.short_description = pgettext_lazy(
        'Timestamp',
        'Timestamps days (PDF)')

    def import_csv(self, request):
        def append_error(type_name, item):
            """Append an error message to the messages list"""
            error_message = pgettext_lazy(
                'Timestamp',
                'Unexpected {TYPE} "{ITEM}"').format(TYPE=type_name,
                                                     ITEM=item)
            if error_message not in error_messages:
                error_messages.append(error_message)
                self.message_user(request, error_message, messages.ERROR)

        if request.method == 'POST':
            # Preload contracts
            contracts = {}
            for item in Contract.objects.all():
                contracts[str(item.id)] = item
            # Preload timestamp directions
            directions = {}
            for item in TimestampDirection.objects.all():
                directions[str(item)] = item
            # Load CSV file content
            csv_file = io.TextIOWrapper(
                request.FILES['csv_file'].file,
                encoding=request.POST['encoding'])
            reader = csv.DictReader(
                csv_file,
                delimiter=request.POST['delimiter'])
            # Load data from CSV
            error_messages = []
            timestamps = []
            for row in reader:
                if row['DIRECTION'] not in directions:
                    append_error('direction', row['DIRECTION'])
                elif row['CONTRACT'] not in contracts:
                    append_error('contract', row['CONTRACT'])
                else:
                    # If no error create a new Timestamp object
                    timestamps.append(Timestamp(
                        contract=contracts[row['CONTRACT']],
                        direction=directions[row['DIRECTION']],
                        date=row['DATE'],
                        time=row['TIME'],
                        description=row['DESCRIPTION']))
            # Save data only if there were not errors
            if not error_messages:
                Timestamp.objects.bulk_create(timestamps)
                self.message_user(request, pgettext_lazy(
                    'Timestamp',
                    'Your CSV file has been imported'))
            return redirect('..')
        return render(request,
                      'utility/import_csv/form.html',
                      {'form': CSVImportForm()})


class TimestampHoursExport(object):
    fields_map = {'DATE': 'date',
                  'COMPANY': 'company',
                  'STRUCTURE': 'structure',
                  'EMPLOYEE': 'employee',
                  'CONTRACT_ID': 'contract_id',
                  'ROLL_NUMBER': 'roll_number',
                  'TIME 1': 'enter',
                  'TIME 1 DESCRIPTION': 'enter_description',
                  'TIME 2': 'exit',
                  'TIME 2 DESCRIPTION': 'exit_description',
                  'DURATION': 'duration',
                  'NOTES': 'notes',
                  }

    def __init__(self, timestamp):
        self.date = timestamp.date
        self.contract = timestamp.contract
        self.structure = timestamp.structure
        self.enter_time = None
        self.enter_description = None
        self.exit_time = None
        self.exit_description = None
        self.other_time = None
        self.other_description = None

    def is_valid(self):
        return any((self.enter_time, self.exit_time, self.other_time))

    def extract(self):
        today = datetime.date.today()
        enter_time = self.enter_time
        exit_time = self.exit_time
        notes = None
        if not self.other_time:
            # Regular enter/exit timestamp
            if not enter_time:
                enter_time = exit_time
                notes = pgettext_lazy('Timestamp', 'Missing enter time')
            if not exit_time:
                exit_time = enter_time
                notes = pgettext_lazy('Timestamp', 'Missing exit time')
            difference = (datetime.datetime.combine(today, exit_time) -
                          datetime.datetime.combine(today, enter_time))
        else:
            # Other timestamp (holiday, etc)
            notes = self.other_description
            difference = None
        return({'date': self.date,
                'company': self.structure.company,
                'structure': self.structure,
                'contract_id': self.contract.pk,
                'employee': self.contract.employee,
                'roll_number': self.contract.roll_number,
                'enter': enter_time,
                'enter_description': self.enter_description,
                'exit': exit_time,
                'exit_description': self.exit_description,
                'duration': difference,
                'other': self.other_time,
                'notes': notes,
                })


class TimestampDaysExport(object):
    fields_map = {'COMPANY': 'company',
                  'STRUCTURE': 'structure',
                  'EMPLOYEE': 'employee',
                  'CONTRACT_ID': 'contract_id',
                  'ROLL_NUMBER': 'roll_number',
                  'WORKING DAYS': 'working_days',
                  }

    def __init__(self, timestamp):
        self.contract = timestamp.contract
        self.structure = timestamp.structure
        self.dates = {}

    def is_valid(self):
        return any((self.dates.keys(), ))

    def extract(self, date_min, date_max, working_short_code):
        results = dict([(day, self.dates.get(day))
                        for day in range(date_min.toordinal(),
                                         date_max.toordinal() + 1)])
        results['company'] = self.structure.company
        results['structure'] = self.structure
        results['contract_id'] = self.contract.pk
        results['employee'] = self.contract.employee
        results['roll_number'] = self.contract.roll_number
        results['working_days'] = list(self.dates.values()).count(
            working_short_code)
        return results
