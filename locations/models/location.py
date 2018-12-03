##
#     Project: Django Milazzo Inn
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
from django.contrib import admin

from .country import Country
from .region import Region

from utility.admin import AdminTextInputFilter


class Location(models.Model):

    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    province = models.CharField(max_length=255,
                                blank=True,
                                null=True)

    class Meta:
        # Define the database table
        db_table = 'locations_locations'
        ordering = ['name']
        unique_together = ('region', 'name')

    def __str__(self):
        if self.province:
            return '{NAME} ({PROVINCE})'.format(NAME=self.name,
                                                PROVINCE=self.province)
        else:
            return '{NAME}'.format(NAME=self.name)


class LocationNameInputFilter(AdminTextInputFilter):
    parameter_name = 'name'
    title = 'name'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__icontains=self.value())


class LocationProvinceInputFilter(AdminTextInputFilter):
    parameter_name = 'province'
    title = 'province'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(province__icontains=self.value())


class LocationAdminCountryFilter(admin.SimpleListFilter):
    title = 'country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        return Country.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region__country=self.value())


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'region', 'country')
    list_filter = (LocationNameInputFilter,
                   LocationProvinceInputFilter,
                   LocationAdminCountryFilter,
                   'region')

    def country(self, instance):
        return instance.region.country
    country.short_description = 'Country'
