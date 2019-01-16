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

from utility.admin_actions import ExportCSVMixin


class Equipment(models.Model):

    structure = models.ForeignKey('Structure',
                                  on_delete=models.PROTECT,
                                  default=0)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Define the database table
        db_table = 'hotels_structure_equipments'
        ordering = ['structure', 'name']
        unique_together = ('structure', 'name')

    def __str__(self):
        return self.name


class EquipmentAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('structure', 'name', 'description')
    list_display_links = ('structure', 'name')
    list_filter = ('structure', )
    actions = ('action_export_csv', )
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'STRUCTURE': 'structure',
        'NAME': 'name',
        'DESCRIPTION': 'description',
        'QUANTITY': 'quantity',
    })
