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

from django.db import models
from django.contrib import admin


class Region(models.Model):

    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country',
                                on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    position = models.ForeignKey('Position',
                                 on_delete=models.PROTECT)
    aliases = models.ManyToManyField('RegionAlias',
                                     db_table='locations_region_aliases',
                                     blank=True)

    class Meta:
        # Define the database table
        db_table = 'locations_regions'
        ordering = ['name']
        unique_together = ('name', 'country')

    def __str__(self):
        return '{COUNTRY} - {NAME}'.format(COUNTRY=self.country.name,
                                           NAME=self.name)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'country', 'position')
    list_filter = ('country', 'position')
