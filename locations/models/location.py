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
from django.utils.translation import pgettext_lazy

from .region import Region

from utility.admin import AdminTextInputFilter
from utility.models import BaseModel, BaseModelAdmin


class Location(BaseModel):
    name = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('Location',
                                                       'name'))
    region = models.ForeignKey('Region',
                               on_delete=models.PROTECT,
                               verbose_name=pgettext_lazy('Location',
                                                          'region'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Location',
                                                              'description'))
    province = models.CharField(max_length=255,
                                blank=True,
                                null=True,
                                verbose_name=pgettext_lazy('Location',
                                                           'province'))

    class Meta:
        # Define the database table
        db_table = 'locations_locations'
        ordering = ['name']
        unique_together = ('region', 'name')
        verbose_name = pgettext_lazy('Location', 'Location')
        verbose_name_plural = pgettext_lazy('Location', 'Locations')

    def __str__(self):
        if self.province:
            return '{NAME} ({PROVINCE})'.format(NAME=self.name,
                                                PROVINCE=self.province)
        else:
            return '{NAME}'.format(NAME=self.name)


class LocationNameInputFilter(AdminTextInputFilter):
    parameter_name = 'name'
    title = pgettext_lazy('Location', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__icontains=self.value())


class LocationProvinceInputFilter(AdminTextInputFilter):
    parameter_name = 'province'
    title = pgettext_lazy('Location', 'province')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(province__icontains=self.value())


class LocationAdminCountryRegionFilter(admin.SimpleListFilter):
    parameter_name = 'region'
    title = pgettext_lazy('Location', 'region')

    def lookups(self, request, model_admin):
        return [(region_id, '{COUNTRY} - {REGION}'.format(
            COUNTRY=region_country, REGION=region_name))
            for region_id, region_name, region_country
            in Region.objects.all().values_list(
            'id', 'name', 'country').order_by('country__name')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region__id=self.value())


class LocationAdmin(BaseModelAdmin):
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'region':
            # Optimize value lookup for field region
            kwargs['queryset'] = Region.objects.all().select_related('country')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def country(self, instance):
        return instance.region.country
    country.short_description = pgettext_lazy('Country', 'Country')
