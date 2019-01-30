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

from django.db import models
from django.contrib import admin

from rangefilter.filter import DateRangeFilter

from . import activity

from ..forms import ActivityRoomInlineForm

from hotels.models import Room, Service

from utility.admin_actions import ExportCSVMixin


class ActivityRoom(models.Model):

    activity = models.ForeignKey('Activity',
                                 on_delete=models.PROTECT)
    room = models.ForeignKey(Room,
                             on_delete=models.PROTECT)
    service = models.ForeignKey(Service,
                                on_delete=models.PROTECT)
    service_qty = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'work_activities_rooms'
        ordering = ['activity', 'room', 'service']
        verbose_name_plural = 'Activity Rooms'
        unique_together = ('activity', 'room', 'service')

    def __str__(self):
        return str(self.pk)


class ActivityRoomAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('activity', 'room', 'service', 'service_qty')
    actions = ('action_export_csv', )
    list_filter = (('activity__date', DateRangeFilter),)
    date_hierarchy = 'activity__date'
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'ACTIVITY': 'activity',
        'ROOM': 'room',
        'SERVICE': 'service',
        'DESCRIPTION': 'description',
    })

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'activity':
            # Optimize value lookup for field activity
            kwargs['queryset'] = (
                activity.Activity.objects.all().select_related(
                    'contract', 'contract__employee', 'contract__company'))
        elif db_field.name == 'room':
            # Optimize value lookup for field room
            if 'object_id' in request.resolver_match.kwargs:
                # Limit rooms to enabled for contract
                object_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = Room.objects.filter(
                    building_id__in=ActivityRoom.objects.get(pk=object_id)
                    .activity.contract.buildings.values('id')
                    ).select_related('building')
            else:
                # During empty adding set no room limit
                kwargs['queryset'] = Room.objects.all().select_related(
                    'building')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ActivityRoomInline(admin.TabularInline):
    model = ActivityRoom
    fields = ('room', 'service', 'service_qty', 'description')
    form = ActivityRoomInlineForm

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ('room', 'service'):
            # dirty trick so queryset is evaluated and cached in .choices
            formfield.choices = formfield.choices
            # Hide add/change/delete buttons
            formfield.widget.can_add_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_delete_related = False
        return formfield

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'room':
            # Optimize value lookup for field room
            if 'object_id' in request.resolver_match.kwargs:
                object_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = Room.objects.filter(
                    building_id__in=activity.Activity.objects.get(pk=object_id)
                    .contract.buildings.values('id')
                    ).select_related('building').prefetch_related('room_type')
            else:
                # During empty adding set no room limit
                kwargs['queryset'] = Room.objects.all().select_related(
                    'building')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
