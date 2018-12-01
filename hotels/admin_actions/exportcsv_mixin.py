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

import csv
import collections

from django.http import HttpResponse


class ExportCSVMixin(object):
    def action_export_csv(self, request, queryset):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename={NAME}.csv'.format(NAME=self.model._meta))
        writer = csv.writer(response, delimiter=';')
        # Write fields names row
        writer.writerow(self.export_csv_fields_map.keys())
        # Write record rows
        for item in queryset:
            row = writer.writerow([getattr(item, field)
                                   for field
                                   in self.export_csv_fields_map.values()])

        return response
    action_export_csv.short_description = 'Export selected rows to CSV'
