##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2019 Fabio Castelli
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

import os
import shutil
import sys

from django.conf import settings

import project

from .api_base import APIv1BaseView


class APIv1UsageView(APIv1BaseView):
    login_with_tablet_id = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Return product data
        context['productname'] = project.PRODUCT_NAME
        context['version'] = project.VERSION
        # Return disk usage
        total_size, used_size, free_size = self.get_disk_usage()
        context['disk total'] = total_size
        context['disk total string'] = self.format_size(total_size)
        context['disk usage'] = used_size
        context['disk usage string'] = self.format_size(used_size)
        context['disk free'] = free_size
        context['disk free string'] = self.format_size(free_size)
        # Return memory RAM usage
        total_size, used_size, free_size = self.get_memory_usage()
        context['memory total'] = total_size
        context['memory total string'] = self.format_size(total_size)
        context['memory usage'] = used_size
        context['memory usage string'] = self.format_size(used_size)
        context['memory free'] = free_size
        context['memory free string'] = self.format_size(free_size)
        # Return database usage
        database_entry = settings.DATABASES['default']
        if database_entry['ENGINE'] == 'django.db.backends.sqlite3':
            total_size = self.get_database_usage()
            context['database size'] = total_size
            context['database size string'] = self.format_size(total_size)
        # Add closing status (to check for transmission errors)
        self.add_status(context)
        return context

    def number_from_unit(self, size, unit):
        """Convert a number from the unit"""
        if unit in ('kb', 'kB', 'KB'):
            return size * 1000
        elif unit in ('mb', 'mB', 'MB'):
            return size * 1000000
        elif unit in ('gb', 'gB', 'GB'):
            return size * 1000000000
        elif unit in ('tb', 'tB', 'TB'):
            return size * 1000000000000

    def format_size(self, size):
        """Format a size using a dynamic unit"""
        if size < 1000:
            return '%i B' % size
        elif 1000 <= size < 1000000:
            return '%.2f KB' % float(size / 1000)
        elif 1000000 <= size < 1000000000:
            return '%.2f MB' % float(size / 1000000)
        elif 1000000000 <= size < 1000000000000:
            return '%.2f GB' % float(size / 1000000000)
        elif 1000000000000 <= size:
            return '%.2f TB' % float(size / 1000000000000)

    def get_disk_usage(self):
        """Return disk usage tuple (total, used, free)"""
        root_directory = '\\' if sys.platform == 'win32' else '/'
        return shutil.disk_usage(root_directory)

    def get_memory_usage(self):
        """Return memory usage tuple (total, used, free)"""
        # noinspection PyBroadException
        try:
            meminfo = {}
            with open('/proc/meminfo') as file:
                for line in file:
                    key, value, *unit = line.strip().split()
                    # For missing unit assume bytes
                    if not unit:
                        unit = ('B', )
                    # Convert size to bytes
                    meminfo[key.rstrip(':')] = self.number_from_unit(
                        size=int(value), unit=unit[0])
            return (meminfo['MemTotal'],
                    meminfo['MemTotal'] - meminfo['MemFree'] -
                    meminfo['Buffers'] - meminfo['Cached'] -
                    meminfo['Slab'],
                    meminfo['MemFree'])
        except Exception:
            return -1, -1, -1

    def get_database_usage(self):
        """Return default database usage"""
        database_entry = settings.DATABASES['default']
        if database_entry['ENGINE'] == 'django.db.backends.sqlite3':
            total_size = os.stat(database_entry['NAME']).st_size
        else:
            total_size = -1
        return total_size
