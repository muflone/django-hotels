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

from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class ContractType(BaseModel):
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=pgettext_lazy('ContractType',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('ContractType',
                                                              'description'))
    daily_hours = models.PositiveIntegerField(verbose_name=pgettext_lazy(
        'ContractType',
        'daily hours'))
    weekly_hours = models.PositiveIntegerField(verbose_name=pgettext_lazy(
        'ContractType',
        'weekly hours'))

    class Meta:
        # Define the database table
        db_table = 'work_contracttype'
        ordering = ['name']
        verbose_name = pgettext_lazy('ContractType', 'Contract type')
        verbose_name_plural = pgettext_lazy('ContractType', 'Contract types')

    def __str__(self):
        return self.name


class ContractTypeAdmin(BaseModelAdmin):
    pass
