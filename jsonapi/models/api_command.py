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


class ApiCommand(BaseModel):
    command_type = models.ForeignKey('ApiCommandType',
                                     on_delete=models.PROTECT,
                                     verbose_name=pgettext_lazy(
                                         'ApiCommand',
                                         'command type'))
    name = models.CharField(max_length=255,
                            default='',
                            verbose_name=pgettext_lazy('ApiCommand',
                                                       'name'))
    context_type = models.ForeignKey('ApiContextType',
                                     on_delete=models.PROTECT,
                                     verbose_name=pgettext_lazy(
                                         'ApiCommand',
                                         'context type'))
    enabled = models.BooleanField(default=True,
                                  verbose_name=pgettext_lazy('ApiCommand',
                                                             'enabled'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('ApiCommand',
                                                              'description'))
    command = models.TextField(blank=True,
                               verbose_name=pgettext_lazy('ApiCommand',
                                                          'command'))
    tablets = models.ManyToManyField('work.tablet',
                                     blank=True,
                                     verbose_name=pgettext_lazy('ApiCommand',
                                                                'tablets'))
    starting = models.DateTimeField(blank=True,
                                    null=True,
                                    default=None,
                                    verbose_name=pgettext_lazy('ApiCommand',
                                                               'starting'))
    ending = models.DateTimeField(blank=True,
                                  null=True,
                                  default=None,
                                  verbose_name=pgettext_lazy('ApiCommand',
                                                             'ending'))
    uses = models.PositiveIntegerField(default=0,
                                       verbose_name=pgettext_lazy('ApiCommand',
                                                                  'uses'))

    class Meta:
        # Define the database table
        db_table = 'api_commands'
        ordering = ['id']
        verbose_name = pgettext_lazy('ApiCommand', 'Api command')
        verbose_name_plural = pgettext_lazy('ApiCommand', 'Api commands')

    def __str__(self):
        return str(self.id)


class ApiCommandNameFilter(AdminTextInputFilter):
    parameter_name = 'name'
    title = pgettext_lazy('ApiCommand', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__icontains=self.value())


class ApiCommandAdmin(BaseModelAdmin):
    pass
