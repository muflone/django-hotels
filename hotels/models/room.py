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
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import path

from .bed_type import BedType
from .building import Building
from .room_type import RoomType
from .structure import Structure

from ..admin_actions import ExportCSVMixin
from ..forms import CSVImportForm, RoomChangeBuildingForm


class Room(models.Model):

    building = models.ForeignKey('Building',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    room_type = models.ForeignKey('RoomType',
                                  on_delete=models.CASCADE)
    bed_type = models.ForeignKey('BedType',
                                 on_delete=models.CASCADE,
                                 default='UNKNOWN')
    phone1 = models.CharField(max_length=255, blank=True)
    seats_base = models.PositiveIntegerField(default=1)
    seats_additional = models.PositiveIntegerField(default=0)

    class Meta:
        # Define the database table
        db_table = 'hotels_rooms'
        ordering = ['building', 'name']
        unique_together = ('building', 'name')

    def __str__(self):
        return '{BUILDING} - {NAME}'.format(BUILDING=self.building.name,
                                            NAME=self.name)


class RoomAdminStructureFilter(admin.SimpleListFilter):
    title = 'structure'
    parameter_name = 'structure'

    def lookups(self, request, model_admin):
        return Structure.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(building__structure=self.value())


class RoomAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('building', 'name', 'room_type')
    list_filter = ('building', RoomAdminStructureFilter, 'room_type')
    change_list_template = 'hotels/change_list.html'
    actions = ('action_export_csv',
               'action_change_building')
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'BUILDING': 'building',
        'NAME': 'name',
        'DESCRIPTION': 'description',
        'ROOM TYPE': 'room_type',
        'BED TYPE': 'bed_type',
        'PHONE1': 'phone1',
        'SEATS BASE': 'seats_base',
        'SEATS ADDITIONAL': 'seats_additional',
    })

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        def append_error(type_name, item):
            """Append an error message to the messages list"""
            error_message = 'Unexpected {TYPE} "{ITEM}"'.format(TYPE=type_name,
                                                                ITEM=item)
            if error_message not in error_messages:
                error_messages.append(error_message)
                self.message_user(request, error_message, messages.ERROR)

        if request.method == 'POST':
            # Preload buildings
            buildings = {}
            for item in Building.objects.all():
                buildings[item.name] = item
            # Preload room types
            room_types = {}
            for item in RoomType.objects.all():
                room_types[item.name] = item
            # Preload bed types
            bed_types = {}
            for item in BedType.objects.all():
                bed_types[item.name] = item
            # Load CSV file content
            csv_file = io.TextIOWrapper(
                request.FILES['csv_file'].file,
                encoding=request.POST['encoding'])
            reader = csv.DictReader(
                csv_file,
                delimiter=request.POST['delimiter'])
            # Load data from CSV
            error_messages = []
            rooms = []
            for row in reader:
                if row['BUILDING'] not in buildings:
                    append_error('building', row['BUILDING'])
                elif row['ROOM TYPE'] not in room_types:
                    append_error('room type', row['ROOM TYPE'])
                elif row['BED TYPE'] not in bed_types:
                    append_error('bed type', row['BED TYPE'])
                else:
                    # If no error create a new Room object
                    rooms.append(Room(building=buildings[row['BUILDING']],
                                      name=row['NAME'],
                                      description=row['DESCRIPTION'],
                                      room_type=room_types[row['ROOM TYPE']],
                                      bed_type=bed_types[row['BED TYPE']],
                                      phone1=row['PHONE1'],
                                      seats_base=row['SEATS BASE'],
                                      seats_additional=row['SEATS ADDITIONAL']
                                      ))
            # Save data only if there were not errors
            if not error_messages:
                Room.objects.bulk_create(rooms)
                self.message_user(request, 'Your CSV file has been imported')
            return redirect('..')
        return render(request,
                      'hotels/form_csv_import.html',
                      {'form': CSVImportForm()})

    def action_change_building(self, request, queryset):
        form = RoomChangeBuildingForm(request.POST)
        if 'action_change_building' in request.POST:
            if form.is_valid():
                building = form.cleaned_data['building']
                queryset.update(building=building)

                self.message_user(request,
                                  'Changed building for {COUNT} rooms'.format(
                                      COUNT=queryset.count()))
                return HttpResponseRedirect(request.get_full_path())

        return render(request,
                      'hotels/form_change_attribute.html',
                      context={'queryset': queryset,
                               'buildings': Building.objects.all(),
                               'form': form,
                               'title': 'Assign the selected rooms to a new '
                                        'building',
                               'question': 'Confirm you want to change the '
                                           'building for the selected rooms?',
                               'items_name': 'Rooms',
                               'action': 'action_change_building',
                               'action_description': 'Change building',
                              })
    action_change_building.short_description = 'Change building'
