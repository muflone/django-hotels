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
import datetime

from django.db import models
from django.contrib import admin

from hotels.models.company import Company

from utility.admin_actions import ExportCSVMixin


class Timestamp(models.Model):

    contract = models.ForeignKey('Contract',
                                 on_delete=models.PROTECT)
    direction = models.CharField(max_length=1,
                                 choices=(('<', 'Enter'),
                                          ('>', 'Exit')))
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'work_timestamps'
        ordering = ['contract', 'date', 'time']

    def __str__(self):
        return '{CONTRACT} {DIRECTION} {DATE} {TIME}'.format(
            CONTRACT=self.contract,
            DIRECTION=self.direction,
            DATE=self.date,
            TIME=self.time)


class TimestampAdminCompanyFilter(admin.SimpleListFilter):
    title = 'company'
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        return Company.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contract__company=self.value())


class TimestampAdmin(admin.ModelAdmin, ExportCSVMixin):

    list_display = ('id', 'first_name', 'last_name', 'direction', 'date',
                    'time')
    list_display_links = ('id', 'first_name', 'last_name')
    list_filter = (TimestampAdminCompanyFilter, )
    readonly_fields = ('id', )
    radio_fields = {'direction': admin.HORIZONTAL}
    actions = ('action_export_csv', )
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'CONTRACT': 'contract',
        'DIRECTION': 'direction',
        'DATE': 'date',
        'TIME': 'time',
        'DESCRIPTION': 'description',
    })

    def first_name(self, instance):
        return instance.contract.employee.first_name
    first_name.short_description = 'First name'

    def last_name(self, instance):
        return instance.contract.employee.last_name
    last_name.last_description = 'Last name'

    def get_fields(self, request, obj=None):
        """Reorder the fields list"""
        fields = super().get_fields(request, obj)
        fields = ['id', ] + [k for k in fields if k not in ('id')]
        return fields
