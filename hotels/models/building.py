##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2019 Fabio Castelli
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


class Building(BaseModel):
    structure = models.ForeignKey('Structure',
                                  on_delete=models.PROTECT,
                                  default=0,
                                  verbose_name=pgettext_lazy('Building',
                                                             'structure'))
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('Building',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Building',
                                                              'description'))
    address = models.TextField(blank=True,
                               verbose_name=pgettext_lazy('Building',
                                                          'address'))
    location = models.ForeignKey('locations.Location',
                                 on_delete=models.PROTECT,
                                 default=0,
                                 verbose_name=pgettext_lazy('Building',
                                                            'location'))
    postal_code = models.CharField(max_length=15,
                                   blank=True,
                                   verbose_name=pgettext_lazy('Building',
                                                              'postal code'))
    phone1 = models.CharField(max_length=255,
                              blank=True,
                              verbose_name=pgettext_lazy('Building',
                                                         'phone 1'))
    phone2 = models.CharField(max_length=255,
                              blank=True,
                              verbose_name=pgettext_lazy('Building',
                                                         'phone 2'))
    fax = models.CharField(max_length=255,
                           blank=True,
                           verbose_name=pgettext_lazy('Building',
                                                      'fax'))
    email = models.CharField(max_length=255,
                             blank=True,
                             verbose_name=pgettext_lazy('Building',
                                                        'email'))
    extras = models.BooleanField(default=False,
                                 verbose_name=pgettext_lazy('Building',
                                                            'extras'))

    class Meta:
        # Define the database table
        db_table = 'hotels_buildings'
        ordering = ['structure', 'name']
        unique_together = ('name', )
        verbose_name = pgettext_lazy('Building', 'Building')
        verbose_name_plural = pgettext_lazy('Building', 'Buildings')

    def __str__(self):
        return self.name


class BuildingAdmin(BaseModelAdmin):
    def brand(self, instance):
        return instance.structure.brand
    brand.short_description = pgettext_lazy('Brand', 'Brand')

    def company(self, instance):
        return instance.structure.company
    company.short_description = pgettext_lazy('Company', 'Company')
