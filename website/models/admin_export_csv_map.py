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

from utility.misc import get_admin_models
from utility.models import BaseModel, BaseModelAdmin


class AdminExportCSVMap(BaseModel):
    admin_models = get_admin_models()

    model = models.CharField(max_length=255,
                             choices=((model_name, model_name)
                                      for model_name
                                      in sorted(admin_models.keys())),
                             verbose_name=pgettext_lazy('AdminExportCSVMap',
                                                        'model'))
    title = models.CharField(max_length=255,
                             verbose_name=pgettext_lazy('AdminExportCSVMap',
                                                        'title'))
    field = models.CharField(max_length=255,
                             verbose_name=pgettext_lazy('AdminExportCSVMap',
                                                        'field'))
    order = models.PositiveIntegerField(verbose_name=pgettext_lazy(
        'AdminExportCSVMap',
        'order'))
    enabled = models.BooleanField(default=True,
                                  verbose_name=pgettext_lazy(
                                      'AdminExportCSVMap',
                                      'enabled'))

    class Meta:
        # Define the database table
        db_table = 'website_admin_export_csv_maps'
        ordering = ['model', 'order', 'title', 'field']
        unique_together = (('model', 'title'),
                           ('model', 'order'))
        verbose_name = pgettext_lazy('AdminExportCSVMap',
                                     'Admin Export CSV Map')
        verbose_name_plural = pgettext_lazy('AdminExportCSVMap',
                                            'Admin Export CSV Maps')

    def __str__(self):
        return '{MODEL} - {FIELD}'.format(MODEL=self.model,
                                          FIELD=self.field)


class AdminExportCSVMapAdmin(BaseModelAdmin):
    pass
