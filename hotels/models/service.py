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


class Service(BaseModel):
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=pgettext_lazy('Service',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Service',
                                                              'description'))
    room_service = models.BooleanField(default=False,
                                       verbose_name=pgettext_lazy(
                                           'Service',
                                           'room service'))
    extra_service = models.BooleanField(default=False,
                                        verbose_name=pgettext_lazy(
                                            'Service',
                                            'extra service'))
    show_in_app = models.BooleanField(default=False,
                                      verbose_name=pgettext_lazy(
                                          'Service',
                                          'show in app'))
    service_type = models.ForeignKey('ServiceType',
                                     on_delete=models.PROTECT,
                                     default=0,
                                     verbose_name=pgettext_lazy(
                                         'Service',
                                         'service type'))

    class Meta:
        # Define the database table
        db_table = 'hotels_services'
        ordering = ['name']
        verbose_name = pgettext_lazy('Service', 'Service')
        verbose_name_plural = pgettext_lazy('Service', 'Services')

    def __str__(self):
        return self.name


class ServiceAdmin(BaseModelAdmin):
    pass
