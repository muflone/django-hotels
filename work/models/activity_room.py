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

from . import activity

from hotels.models import Room, RoomService, Service

from utility.admin_actions import ExportCSVMixin


class ActivityRoom(models.Model):

    activity = models.ForeignKey('Activity',
                                 on_delete=models.PROTECT)
    room = models.ForeignKey(Room,
                             on_delete=models.PROTECT)
    service = models.ForeignKey(Service,
                                on_delete=models.PROTECT)
    class Meta:
        # Define the database table
        db_table = 'work_activities_rooms'
        ordering = ['activity', 'room', 'service']
        verbose_name_plural = 'Activity Rooms'
        unique_together = ('activity', 'room', 'service')

    def __str__(self):
        return '{ACTIVITY} {ROOM} {SERVICE}'.format(
            ACTIVITY=self.activity,
            ROOM=self.room,
            SERVICE=self.service)


class ActivityRoomAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('activity', 'room', 'service')
    actions = ('action_export_csv', )
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'ACTIVITY': 'activity',
        'ROOM': 'room',
        'SERVICE': 'service',
    })

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'activity':
            # Optimize value lookup for field activity
            kwargs['queryset'] = activity.Activity.objects.all().select_related(
                'contract', 'contract__employee', 'contract__company')
        elif db_field.name == 'room':
            # Optimize value lookup for field service
            kwargs['queryset'] = Room.objects.all().select_related(
                'building', 'building__structure')
        elif db_field.name == 'service':
            # Optimize value lookup for field service
            kwargs['queryset'] = Service.objects.filter(
                name__in=RoomService.objects.values_list('service__name'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ActivityRoomInline(admin.TabularInline):
    model = ActivityRoom

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'activity':
            # Optimize value lookup for field activity
            kwargs['queryset'] = activity.Activity.objects.all().select_related(
                'contract', 'contract__employee', 'contract__company')
        elif db_field.name == 'room':
            # Optimize value lookup for field room
            kwargs['queryset'] = Room.objects.all().select_related(
                'building', 'building__structure')
        elif db_field.name == 'service':
            # Optimize value lookup for field service
            kwargs['queryset'] = Service.objects.filter(
                name__in=RoomService.objects.values_list('service__name'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
