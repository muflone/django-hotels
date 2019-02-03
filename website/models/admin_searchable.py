##
#     Project: Django Hotels
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

from django.db import models

from utility.misc import get_admin_models
from utility.models import BaseModel, BaseModelAdmin


class AdminSearchable(BaseModel):

    admin_models = get_admin_models()

    model = models.CharField(max_length=255,
                             choices=((model_name, model_name)
                                      for model_name
                                      in sorted(admin_models.keys())))
    field = models.CharField(max_length=255)
    ref_model = models.CharField(max_length=255,
                                 choices=((model_name, model_name)
                                          for model_name
                                          in sorted(admin_models.keys())))
    ref_field = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    use_select2 = models.BooleanField()

    class Meta:
        # Define the database table
        db_table = 'website_admin_searchable'
        ordering = ['model', 'field']
        unique_together = ('model', 'field')

    def __str__(self):
        return '{MODEL} - {FIELD}'.format(MODEL=self.model,
                                          FIELD=self.field)

    def get_model(self):
        return self.admin_models[self.model]

    def get_ref_model(self):
        return self.admin_models[self.ref_model]


class AdminSearchableAdmin(BaseModelAdmin):
    list_display = ('model', 'field', 'use_select2', 'description')
