##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2019 Fabio Castelli
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
import datetime
import json

from django.contrib.admin import SimpleListFilter
from django.db import models
from django.utils.http import urlunquote
from django.utils.translation import pgettext_lazy

from hotels.models import Room, Service

from utility.admin import AdminTextInputFilter
from utility.models import BaseModel, BaseModelAdmin

from work.models import Contract, Tablet, TimestampDirection


class ApiLog(BaseModel):
    date = models.DateField(verbose_name=pgettext_lazy('ApiLog',
                                                       'date'))
    time = models.TimeField(verbose_name=pgettext_lazy('ApiLog',
                                                       'time'))
    message_level = models.PositiveIntegerField(verbose_name=pgettext_lazy(
        'ApiLog',
        'message level'))
    method = models.CharField(max_length=255,
                              verbose_name=pgettext_lazy('ApiLog',
                                                         'metod'))
    path = models.CharField(max_length=255,
                            verbose_name=pgettext_lazy('ApiLog',
                                                       'path'))
    raw_uri = models.TextField(blank=False,
                               verbose_name=pgettext_lazy('ApiLog',
                                                          'raw uri'))
    url_name = models.CharField(max_length=255,
                                verbose_name=pgettext_lazy('ApiLog',
                                                           'url name'))
    func_name = models.CharField(max_length=255,
                                 verbose_name=pgettext_lazy('ApiLog',
                                                            'function name'))
    remote_addr = models.CharField(max_length=255,
                                   blank=True,
                                   verbose_name=pgettext_lazy(
                                       'ApiLog',
                                       'remote address'))
    forwarded_for = models.CharField(max_length=255,
                                     blank=True,
                                     verbose_name=pgettext_lazy(
                                         'ApiLog',
                                         'forwarded for'))
    user_agent = models.CharField(max_length=255,
                                  blank=True,
                                  verbose_name=pgettext_lazy('ApiLog',
                                                             'user agent'))
    client_agent = models.CharField(max_length=255,
                                    blank=True,
                                    verbose_name=pgettext_lazy('ApiLog',
                                                               'client agent'))
    client_version = models.CharField(max_length=255,
                                      blank=True,
                                      verbose_name=pgettext_lazy(
                                          'ApiLog',
                                          'client version'))
    user = models.CharField(max_length=255,
                            blank=True,
                            verbose_name=pgettext_lazy('ApiLog',
                                                       'user'))
    tablet_id = models.PositiveIntegerField(verbose_name=pgettext_lazy(
        'ApiLog',
        'tablet id'))
    kwargs = models.TextField(blank=True,
                              verbose_name=pgettext_lazy('ApiLog',
                                                         'keyword arguments'))
    args = models.TextField(blank=True,
                            verbose_name=pgettext_lazy('ApiLog',
                                                       'arguments'))
    extra = models.TextField(blank=True,
                             verbose_name=pgettext_lazy('ApiLog',
                                                        'extra'))
    api_version = models.PositiveIntegerField(verbose_name=pgettext_lazy(
        'ApiLog',
        'api version'))

    class Meta:
        # Define the database table
        db_table = 'api_log'
        ordering = ['-date', '-time', '-id']
        verbose_name = pgettext_lazy('ApiLog', 'Api log')
        verbose_name_plural = pgettext_lazy('ApiLog',
                                            'Api logs')

    def __str__(self):
        return str(self.id)


class RemoteAddrInputFilter(AdminTextInputFilter):
    parameter_name = 'remote_addr'
    title = pgettext_lazy('ApiLog', 'remote address')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(remote_addr__icontains=self.value())


class ForwardedForInputFilter(AdminTextInputFilter):
    parameter_name = 'forwarded_for'
    title = pgettext_lazy('ApiLog', 'forwarded for')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(forwarded_for__icontains=self.value())


class UserAgentInputFilter(AdminTextInputFilter):
    parameter_name = 'user_agent'
    title = pgettext_lazy('ApiLog', 'user agent')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_agent__icontains=self.value())


class TabletIDFilter(SimpleListFilter):
    parameter_name = 'tablet_id'
    title = pgettext_lazy('ApiLog', 'tablet id')

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
    readonly_fields = ('explanation', )

    def explanation(self, instance):
        """Explanation text for log"""
        result = ''
        if instance.id:
            details = (json.loads(instance.kwargs.replace('\'', '"'))
                       if instance.kwargs else {})
            if instance.func_name == 'APIv1PutActivity':
                contract = Contract.objects.get(
                    id=details['contract_id'])
                employee = contract.employee
                room = Room.objects.get(id=details['room_id'])
                service = Service.objects.get(id=details['service_id'])
                date = datetime.datetime.fromtimestamp(
                    int(details['datetime'])).strftime('%F')
                description = urlunquote(
                    details.get('description', '')).replace('+', ' ')
                result = ('Tablet {TABLET}\n'
                          'Contract: {CONTRACT}\n'
                          'Employee: {FIRST_NAME} {LAST_NAME}\n'
                          'Structure: {STRUCTURE}\n'
                          'Building: {BUILDING}\n'
                          'Room: {ROOM}\n'
                          'Service: {SERVICE}\n'
                          'Date: {DATE}\n'
                          'Description: {DESCRIPTION}'
                          ''.format(TABLET=instance.tablet_id,
                                    CONTRACT=contract.pk,
                                    FIRST_NAME=employee.first_name,
                                    LAST_NAME=employee.last_name,
                                    STRUCTURE=room.building.structure.name,
                                    BUILDING=room.building.name,
                                    ROOM=room.name,
                                    SERVICE=service.name,
                                    DATE=date,
                                    DESCRIPTION=description))
            elif instance.func_name == 'APIv1PutTimestamp':
                contract = Contract.objects.get(
                    id=details['contract_id'])
                employee = contract.employee
                direction = TimestampDirection.objects.get(
                    id=details['direction_id'])
                date = datetime.datetime.fromtimestamp(
                    int(details['datetime'])).strftime('%F %T')
                description = urlunquote(
                    details.get('description', '')).replace('+', ' ')
                result = ('Tablet {TABLET}\n'
                          'Contract: {CONTRACT}\n'
                          'Employee: {FIRST_NAME} {LAST_NAME}\n'
                          'Direction: {DIRECTION}\n'
                          'Date: {DATE}\n'
                          'Description: {DESCRIPTION}'
                          ''.format(TABLET=instance.tablet_id,
                                    CONTRACT=contract.pk,
                                    FIRST_NAME=employee.first_name,
                                    LAST_NAME=employee.last_name,
                                    DIRECTION=direction.name,
                                    DATE=date,
                                    DESCRIPTION=description))
            elif instance.func_name == 'APIv1DatesView' and details:
                result = ('Tablet {TABLET}\n'
                          'Tablet Date: {DATE}\n'
                          'Tablet Time: {TIME}\n'
                          'Tablet Timezone: {TIMEZONE} ({TZ_ID})'
                          ''.format(TABLET=instance.tablet_id,
                                    DATE=details['tablet_date'],
                                    TIME=details['tablet_time'],
                                    TIMEZONE=details['tablet_timezone'],
                                    TZ_ID=details['tablet_timezone_id']))
            elif instance.func_name in ('APIv1StatusView', 'APIv1GetView'):
                result = ('Tablet {TABLET}'
                          ''.format(TABLET=instance.tablet_id))
        return result
    explanation.short_description = pgettext_lazy('ApiLog', 'Explanation')
