##
#     Project: Django Hotels
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

from django.db import models

from rangefilter.filter import DateRangeFilter

from . import activity_room
from .contract import Contract

from utility.models import BaseModel, BaseModelAdmin


class Activity(BaseModel):

    contract = models.ForeignKey('Contract',
                                 on_delete=models.PROTECT)
    date = models.DateField()

    class Meta:
        # Define the database table
        db_table = 'work_activities'
        ordering = ['-date', 'contract__employee']
        verbose_name_plural = 'Activities'
        unique_together = ('contract', 'date')

    def __str__(self):
        return '{CONTRACT} {DATE}'.format(
            CONTRACT=self.contract,
            DATE=self.date)


class ActivityAdmin(BaseModelAdmin):
    list_filter = (('date', DateRangeFilter),
                   'contract__company', 'contract__employee')
    date_hierarchy = 'date'
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'CONTRACT': 'contract',
        'DATE': 'date',
    })

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'contract':
            # Optimize value lookup for field contract
            kwargs['queryset'] = Contract.objects.all().select_related(
                'employee', 'company')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ActivityInLinesProxy(Activity):
    class Meta:
        verbose_name_plural = 'Activities with Rooms'
        proxy = True


class ActivityInLinesAdmin(BaseModelAdmin):
    list_filter = (('date', DateRangeFilter),
                   'contract__company', 'contract__employee')
    inlines = [activity_room.ActivityRoomInline, ]
    date_hierarchy = 'date'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'contract':
            # Optimize value lookup for field contract
            kwargs['queryset'] = Contract.objects.all().select_related(
                'employee', 'company')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
