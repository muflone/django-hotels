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

from utility.admin import AdminTextInputFilter
from utility.models import BaseModel, BaseModelAdmin


class AdminOption(BaseModel):
    section = models.CharField(max_length=255,
                               verbose_name=pgettext_lazy('AdminOption',
                                                          'section'))
    group = models.CharField(max_length=255,
                             default='main',
                             verbose_name=pgettext_lazy('AdminOption',
                                                        'group'))
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('AdminOption',
                                                       'name'))
    enabled = models.BooleanField(default=True,
                                  verbose_name=pgettext_lazy('AdminOption',
                                                             'enabled'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('AdminOption',
                                                              'description'))
    value = models.TextField(blank=True,
                             verbose_name=pgettext_lazy('AdminOption',
                                                        'value'))

    class Meta:
        # Define the database table
        db_table = 'website_admin_options'
        ordering = ['section', 'group', 'name']
        unique_together = ('section', 'group', 'name')
        verbose_name = pgettext_lazy('AdminOption',
                                     'Admin Option')
        verbose_name_plural = pgettext_lazy('AdminOption',
                                            'Admin Options')

    def __str__(self):
        return '{SECTION} - {GROUP} - {NAME}'.format(SECTION=self.section,
                                                     GROUP=self.group,
                                                     NAME=self.name)


class AdminOptionNameFilter(AdminTextInputFilter):
    parameter_name = 'name'
    title = pgettext_lazy('AdminOption', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__icontains=self.value())


class AdminOptionAdmin(BaseModelAdmin):
    pass
