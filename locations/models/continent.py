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


class Continent(BaseModel):
    name = models.CharField(max_length=255,
                            primary_key=True,
                            verbose_name=pgettext_lazy('Continent',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Continent',
                                                              'description'))

    class Meta:
        # Define the database table
        db_table = 'locations_continents'
        ordering = ['name']
        verbose_name = pgettext_lazy('Continent', 'Continent')
        verbose_name_plural = pgettext_lazy('Continent', 'Continents')

    def __str__(self):
        return self.name


class ContinentAdmin(BaseModelAdmin):
    pass
