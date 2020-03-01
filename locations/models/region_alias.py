##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2020 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class RegionAlias(BaseModel):
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('RegionAlias',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('RegionAlias',
                                                              'description'))
    country = models.ForeignKey('Country',
                                on_delete=models.PROTECT,
                                verbose_name=pgettext_lazy('RegionAlias',
                                                           'country'))

    class Meta:
        # Define the database table
        db_table = 'locations_regions_aliases'
        ordering = ['name']
        unique_together = ('name', 'country')
        verbose_name = pgettext_lazy('RegionAlias', 'Region alias')
        verbose_name_plural = pgettext_lazy('RegionAlias', 'Region aliases')

    def __str__(self):
        return '{COUNTRY} - {NAME}'.format(COUNTRY=self.country.name,
                                           NAME=self.name)


class RegionAliasAdmin(BaseModelAdmin):
    pass
