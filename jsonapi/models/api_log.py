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

from django.contrib.admin import SimpleListFilter
from django.db import models

from utility.admin import AdminTextInputFilter
from utility.models import BaseModel, BaseModelAdmin

from work.models import Tablet


class ApiLog(BaseModel):

    date = models.DateField()
    time = models.TimeField()
    message_level = models.PositiveIntegerField()
    method = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    raw_uri = models.TextField(blank=False)
    url_name = models.CharField(max_length=255)
    func_name = models.CharField(max_length=255)
    remote_addr = models.CharField(max_length=255, blank=True)
    forwarded_for = models.CharField(max_length=255, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    client_agent = models.CharField(max_length=255, blank=True)
    client_version = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, blank=True)
    tablet_id = models.PositiveIntegerField()
    kwargs = models.TextField(blank=True)
    args = models.TextField(blank=True)
    extra = models.TextField(blank=True)
    api_version = models.PositiveIntegerField()

    class Meta:
        # Define the database table
        db_table = 'api_log'
        ordering = ['date', 'time', 'id']

    def __str__(self):
        return str(self.id)


class RemoteAddrInputFilter(AdminTextInputFilter):
    parameter_name = 'remote_addr'
    title = 'remote address'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(remote_addr__icontains=self.value())


class ForwardedForInputFilter(AdminTextInputFilter):
    parameter_name = 'forwarded_for'
    title = 'forwarded for'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(forwarded_for__icontains=self.value())


class UserAgentInputFilter(AdminTextInputFilter):
    parameter_name = 'user_agent'
    title = 'user agent'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_agent__icontains=self.value())


class TabletIDFilter(SimpleListFilter):
    parameter_name = 'tablet_id'
    title = 'tablet'

    def lookups(self, request, model_admin):
        # List only used tablets
        return [(tablet.id,
                 str(tablet) if tablet.id > 0 else tablet.description)
                for tablet in Tablet.objects.filter(
                    id__in=ApiLog.objects.values('tablet_id'))]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tablet_id__exact=self.value())
        else:
            return queryset


class ApiLogAdmin(BaseModelAdmin):
    pass
