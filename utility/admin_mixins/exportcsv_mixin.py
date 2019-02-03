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

import csv

from django.http import HttpResponse


class ExportCSVMixin(object):
    export_csv_fields_map = {}

    def __init__(self):
        """Add Export rows to CSV action to the Admin model"""
        if 'action_export_csv' not in self.actions:
            self.__class__.actions = ('action_export_csv', *self.actions)

    def action_export_csv(self, request, queryset):
        """Export a queryset in CSV format"""
        data = []
        for row in queryset:
            item = {}
            for key in self.export_csv_fields_map.keys():
                field = self.export_csv_fields_map[key]
                item[field] = (getattr(row, field)
                               if not callable(getattr(row, field))
                               else getattr(row, field)())
            data.append(item)
        return self.do_export_data_to_csv(
            data=data,
            fields_map=self.export_csv_fields_map,
            filename=self.model._meta)
    action_export_csv.short_description = 'Export selected rows to CSV'

    def do_export_data_to_csv(self, data, fields_map, filename):
        """Export a list of dict items in CSV format"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename={FILENAME}.csv'.format(FILENAME=filename))
        writer = csv.writer(response, delimiter=';')
        # Write fields names row
        writer.writerow(fields_map.keys())
        # Write record rows
        for item in data:
            writer.writerow([item[field] for field in fields_map.values()])

        return response
