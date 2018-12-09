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


class ContractAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ('first_name', 'last_name', 'company', 'roll_number',
                    'status')
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
