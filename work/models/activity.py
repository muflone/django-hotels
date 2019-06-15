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

import datetime
from collections import defaultdict

from django.db import models
from django.template.response import TemplateResponse
from django.urls import path

from . import activity_room
from .contract import Contract

from hotels.models import ServiceType

from utility.misc import month_start, month_end
from utility.models import BaseModel, BaseModelAdmin


class Activity(BaseModel):

    contract = models.ForeignKey('Contract',
                                 on_delete=models.PROTECT)
    date = models.DateField()

    class Meta:
        # Define the database table
        db_table = 'work_activities'
        ordering = ['-date', 'contract__employee']
        verbose_name_plural = 'Activities'
        unique_together = ('contract', 'date')

    def __str__(self):
        return '{CONTRACT} {DATE}'.format(
            CONTRACT=self.contract,
            DATE=self.date)


class ActivityAdmin(BaseModelAdmin):
    change_form_template = 'work/admin_activity_change.html'
    date_hierarchy = 'date'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'contract':
            # Optimize value lookup for field contract
            kwargs['queryset'] = Contract.objects.all().select_related(
                'employee', 'company')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_urls(self):
        urls = [
            path('<int:activity_id>/export_monthly', self.export_monthly),
        ] + super().get_urls()
        return urls

    def export_monthly(self, request, activity_id):
        # Get dates from selected activity
        activity_ref = Activity.objects.get(pk=activity_id)
        date_min = month_start(activity_ref.date)
        date_max = month_end(activity_ref.date)

        # Annotate count for each service type
        activities = Activity.objects.filter(
            contract=activity_ref.contract,
            date__gte=date_min,
            date__lte=date_max).order_by('date')
        service_types = (ServiceType.objects.filter(show_in_reports=True)
                         .order_by('order'))
        for service_type in service_types:
            # Prepare services for export
            ActivityDayExport.fields_map[service_type.name] = (
                'count_{TYPE}'.format(TYPE=service_type.name))
            # Maybe too little readable!
            # Add a field called count_SERVICE_TYPE__NAME consisting of
            # the count of the ActivityRoom rows with the same Service Type id
            # For example:
            # .annotate(count_other=models.Count('activityroom', filter=
            #           models.Q(activityroom__service__service_type_id=
            #                    service_type.pk)))
            dict_sub_filter = {'activityroom__service__service_type_id':
                               service_type.pk}
            dict_annotate = {'count_{TYPE}'.format(TYPE=service_type.name):
                             models.Count('activityroom', filter=models.Q(
                                **dict_sub_filter))}
            activities = activities.annotate(**dict_annotate)
        # Loop over days
        results = []
        for day in range(date_min.toordinal(), date_max.toordinal() + 1):
            activity_export = ActivityDayExport(contract=activity_ref.contract,
                                                service_types=service_types)
            # Get the daily activity
            activity = activities.filter(date=datetime.date.fromordinal(day))
            if activity:
                # Add each service counts
                for service_type in service_types:
                    count_name = 'count_{TYPE}'.format(TYPE=service_type.name)
                    activity_export.counts[count_name] = getattr(activity[0],
                                                                 count_name)
            results.append(activity_export.extract(
                date=datetime.date.fromordinal(day)))
        # Export data to CSV format
        return self.do_export_data_to_csv(
            data=results,
            fields_map=ActivityDayExport.fields_map,
            filename='export_activities_monthly')


class ActivityInLinesProxy(Activity):
    class Meta:
        verbose_name_plural = 'Activities with Rooms'
        proxy = True


class ActivityInLinesAdmin(BaseModelAdmin):
    inlines = [activity_room.ActivityRoomInline, ]
    date_hierarchy = 'date'
    actions = ('action_report_daily', )

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'contract':
            # Optimize value lookup for field contract
            kwargs['queryset'] = Contract.objects.all().select_related(
                'employee', 'company')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def action_report_daily(self, request, queryset):
        queryset = queryset.order_by('date', 'contract')
        # Cycle each unique date/contract
        results = []
        grand_totals = defaultdict(int)
        for activity in queryset:
            services = []
            totals = defaultdict(int)
            for activityroom in activity_room.ActivityRoom.objects.filter(
                    activity=activity).order_by(
                    'room__building__name', 'room__name'):
                services.append({'building': activityroom.room.building.name,
                                 'room': activityroom.room.name,
                                 'service': activityroom.service.name
                                 })
                totals[activityroom.service.name] += 1
                grand_totals[activityroom.service.name] += 1
            results.append({'activity': str(activity),
                            'services': services,
                            'totals': ['%s: %d' % (i[0], i[1])
                                       for i in totals.items()]
                            })
        # Export report
        context = dict(
            # Include common variables for rendering the admin template
            self.admin_site.each_context(request),
            results=results,
            grand_totals=sorted(['%s: %d' % (i[0], i[1])
                                for i in grand_totals.items()])
        )
        response = TemplateResponse(request,
                                    'work/admin_action_report_daily.html',
                                    context)
        return response
    action_report_daily.short_description = 'Report daily activities'


class ActivityDayExport(object):
    fields_map = {'DATE': 'date',
                  'COMPANY': 'company',
                  'EMPLOYEE': 'employee',
                  'CONTRACT_ID': 'contract_id',
                  'ROLL_NUMBER': 'roll_number',
                  }

    def __init__(self, contract, service_types):
        self.contract = contract
        self.services = []
        # Initialize services counts to zero
        self.counts = {}
        for service_type in service_types:
            self.services.append(service_type.name)
            self.counts['count_{TYPE}'.format(TYPE=service_type.name)] = 0

    def extract(self, date):
        results = {'date': date,
                   'company': self.contract.company,
                   'contract_id': self.contract.pk,
                   'employee': self.contract.employee,
                   'roll_number': self.contract.roll_number,
                   }
        # Append services counts
        results = dict(results, **self.counts)
        return(results)
