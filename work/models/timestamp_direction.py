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

from django.db import models

from utility.models import BaseModel, BaseModelAdmin


class TimestampDirection(BaseModel):

    name = models.CharField(max_length=255, unique=True)
    short_code = models.CharField(max_length=3, blank=True)
    description = models.TextField(blank=True)
    type_enter = models.BooleanField()
    type_exit = models.BooleanField()

    class Meta:
        # Define the database table
        db_table = 'work_timestamp_directions'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    @classmethod
    def get_enter_direction(cls):
        return cls.objects.get(type_enter=True)

    @classmethod
    def get_exit_direction(cls):
        return cls.objects.get(type_exit=True)


class TimestampDirectionAdmin(BaseModelAdmin):
    pass
