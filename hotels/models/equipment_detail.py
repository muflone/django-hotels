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


class EquipmentDetail(BaseModel):
    date = models.DateField(verbose_name=pgettext_lazy('EquipmentDetail',
                                                       'date'))
    structure = models.ForeignKey('Structure',
                                  on_delete=models.PROTECT,
                                  default=0,
                                  verbose_name=pgettext_lazy('EquipmentDetail',
                                                             'structure'))
    item = models.ForeignKey('EquipmentItem',
                             on_delete=models.PROTECT,
                             default=0,
                             verbose_name=pgettext_lazy('EquipmentDetail',
                                                        'item'))
    direction = models.ForeignKey('EquipmentDirection',
                                  on_delete=models.PROTECT,
                                  default=0,
                                  verbose_name=pgettext_lazy('EquipmentDetail',
                                                             'direction'))
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name=pgettext_lazy(
                                               'EquipmentDetail',
                                               'quantity'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy(
                                       'EquipmentDetail',
                                       'description'))

    class Meta:
        # Define the database table
        db_table = 'hotels_equipment_details'
        ordering = ['date', 'structure']
        verbose_name = pgettext_lazy('EquipmentDetail',
                                     'Equipment detail')
        verbose_name_plural = pgettext_lazy('EquipmentDetail',
                                            'Equipment details')

    def __str__(self):
        return '{STRUCTURE} - {ITEM}'.format(STRUCTURE=self.structure,
                                             ITEM=self.item)


class EquipmentDetailAdmin(BaseModelAdmin):
    pass
