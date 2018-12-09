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
import os.path

from django.conf import settings
from django.db import models
from django.contrib import admin
from django.utils.html import mark_safe

from hotels.models.company import Company

from utility.admin_actions import ExportCSVMixin


class Contract(models.Model):

    employee = models.ForeignKey('Employee',
                                 on_delete=models.PROTECT)
    company = models.ForeignKey('hotels.Company',
                                on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    contract_type = models.ForeignKey('ContractType',
                                      on_delete=models.PROTECT)
    job_type = models.ForeignKey('JobType',
                                 on_delete=models.PROTECT)
    roll_number = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    level = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    associated = models.BooleanField()

    class Meta:
        # Define the database table
        db_table = 'work_contract'
        ordering = ['company', 'employee', 'end_date']
        unique_together = (('company', 'employee', 'roll_number'),
                           ('company', 'employee', 'start_date', 'end_date'))

    def __str__(self):
        return '{COMPANY} {EMPLOYEE} {ROLL_NUMBER} {STATUS}'.format(
            COMPANY=self.company,
            EMPLOYEE=self.employee,
            ROLL_NUMBER=self.roll_number,
            STATUS=self.status)


class ContractAdminCompanyFilter(admin.SimpleListFilter):
    title = 'company'
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        return Company.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(company=self.value())


class ContractAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('first_name', 'last_name', 'company', 'roll_number',
                    'status', 'photo_thumbnail')
    list_display_links = ('first_name', 'last_name')
    list_filter = (ContractAdminCompanyFilter, )
    actions = ('action_export_csv', )
    # Define fields and attributes to export rows to CSV
    export_csv_fields_map = collections.OrderedDict({
        'EMPLOYEE': 'employee',
        'COMPANY': 'company',
        'DESCRIPTION': 'description',
        'CONTRACT TYPE': 'contract_type',
        'JOB TYPE': 'job_type',
        'ROLL NUMBER': 'roll_number',
        'START DATE': 'start_date',
        'END DATE': 'end_date',
        'LEVEL': 'level',
        'STATUS': 'status',
        'ASSOCIATED': 'associated',
    })

    def first_name(self, instance):
        return instance.employee.first_name
    first_name.short_description = 'First name'

    def last_name(self, instance):
        return instance.employee.last_name
    last_name.last_description = 'Last name'

    def detail_photo_image(self, instance, width, height):
        if instance.employee.photo.url.startswith(
                os.path.join(settings.MEDIA_URL, 'standard%3A')):
            iconset = instance.employee.photo.url.split('%3A', 1)[1]
            base_url = os.path.join(settings.STATIC_URL,
                                    'hotels/images/{ICONSET}/'
                                    '{SIZE}x{SIZE}.png')
            url_thumbnail = base_url.format(ICONSET=iconset, SIZE=width)
            url_image = base_url.format(ICONSET=iconset, SIZE=512)
        else:
            # Show image
            url_thumbnail = instance.employee.photo.url
            url_image = url_thumbnail

        return mark_safe('<a href="{url}" target="_blank">'
                         '<img src="{thumbnail}" '
                         'width="{width}" '
                         'height={height} />'.format(url=url_image,
                                                     thumbnail=url_thumbnail,
                                                     width=width,
                                                     height=height))

    def photo_thumbnail(self, instance):
        return self.detail_photo_image(instance, 48, 48)
