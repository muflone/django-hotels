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
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.utils.translation import pgettext_lazy

from .service import Service

from utility.models import BaseModel, BaseModelAdmin


class ServiceExtra(BaseModel):
    structure = models.ForeignKey('Structure',
                                  on_delete=models.PROTECT,
                                  default=0,
                                  verbose_name=pgettext_lazy('ServiceExtra',
                                                             'structure'))
    service = models.ForeignKey('Service',
                                on_delete=models.PROTECT,
                                default=0,
                                verbose_name=pgettext_lazy('ServiceExtra',
                                                           'service'))
    price = models.DecimalField(max_digits=11,
                                decimal_places=2,
                                default=0.0,
                                validators=[MinValueValidator(0.00)],
                                verbose_name=pgettext_lazy('ServiceExtra',
                                                           'price'))

    class Meta:
        # Define the database table
        db_table = 'hotels_services_extra'
        ordering = ['structure', 'service']
        unique_together = ('structure', 'service')
        verbose_name = pgettext_lazy('ServiceExtra', 'Service extra')
        verbose_name_plural = pgettext_lazy('ServiceExtra', 'Service extras')

    def __str__(self):
        return '{STRUCTURE} - {SERVICE}'.format(STRUCTURE=self.structure,
                                                SERVICE=self.service)


class ServiceExtraService(admin.SimpleListFilter):
    title = pgettext_lazy('ServiceExtra', 'service')
    parameter_name = 'service'

    def lookups(self, request, model_admin):
        return Service.objects.filter(extra_service=True).values_list('id',
                                                                      'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(service__id=self.value())


class ServiceExtraAdmin(BaseModelAdmin):
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'service':
            # Optimize value lookup for field service
            kwargs['queryset'] = Service.objects.filter(extra_service=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
