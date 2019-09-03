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
import collections
import datetime
from collections import defaultdict
import sys

from django.db import models
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import pgettext_lazy

from . import activity_room
from .contract import Contract

from hotels.models import Service, ServiceType, Structure

from utility.misc import (get_admin_options,
                          month_start, month_end,
                          xhtml2pdf_render_from_template_response)
from utility.models import BaseModel, BaseModelAdmin


class Activity(BaseModel):
    contract = models.ForeignKey('Contract',
                                 on_delete=models.PROTECT,
                                 verbose_name=pgettext_lazy('Activity',
                                                            'contract'))
    date = models.DateField(verbose_name=pgettext_lazy('Activity',
                                                       'date'))

    class Meta:
        # Define the database table
        db_table = 'work_activities'
        ordering = ['-date', 'contract__employee']
        unique_together = ('contract', 'date')
        verbose_name = pgettext_lazy('Activity',
                                     'Activity')
        verbose_name_plural = pgettext_lazy('Activity',
                                            'Activities')

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
        verbose_name = pgettext_lazy('Activity',
                                     'Activity with Rooms')
        verbose_name_plural = pgettext_lazy('Activity',
                                            'Activities with Rooms')
        proxy = True


class ActivityInLinesAdmin(BaseModelAdmin):
    inlines = [activity_room.ActivityRoomInline]
    date_hierarchy = 'date'
    actions = ('action_daily_activities_html',
               'action_daily_activities_pdf',
               'action_monthly_activities_html',
               'action_monthly_activities_pdf')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'contract':
            # Optimize value lookup for field contract
            kwargs['queryset'] = Contract.objects.all().select_related(
                'employee', 'company')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_daily_activities(self, request, queryset):
        queryset = queryset.order_by('date', 'contract')
        # Cycle each unique date/contract
        results = []
        grand_totals = defaultdict(int)
        for activity in queryset:
            services = []
            totals = defaultdict(int)
            for activityroom in activity_room.ActivityRoom.objects.filter(
                    activity=activity).select_related(
                    'room', 'room__building', 'service').order_by(
                    'room__building__name', 'room__name'):
                services.append({'building': activityroom.room.building.name,
                                 'room': activityroom.room.name,
                                 'service': activityroom.service.name,
                                 'service_id': activityroom.service_id,
                                 'description': activityroom.description
                                 })
                totals[activityroom.service.name] += 1
                grand_totals[activityroom.service.name] += 1
            results.append({'company': activity.contract.company,
                            'employee': activity.contract.employee,
                            'date': activity.date,
                            'activity': str(activity),
                            'services': services,
                            'totals': sorted(['%s: %d' % (i[0], i[1])
                                              for i in totals.items()])
                            })
        # Export data
        context = dict(
            # Include common variables for rendering the admin template
            self.admin_site.each_context(request),
            results=results,
            grand_totals=sorted(['%s: %d' % (i[0], i[1])
                                for i in grand_totals.items()]),
            services=Service.objects.values('id', 'name')
        )
        return context

    def action_daily_activities_html(self, request, queryset):
        context = self.get_daily_activities(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        response = TemplateResponse(request,
                                    'work/activities_daily/admin.html',
                                    context)
        return response
    action_daily_activities_html.short_description = pgettext_lazy(
        'Activity',
        'Daily activities (HTML)')

    def action_daily_activities_pdf(self, request, queryset):
        context = self.get_daily_activities(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        response = xhtml2pdf_render_from_template_response(
            response=TemplateResponse(request,
                                      'work/activities_daily/pdf.html',
                                      context),
            filename='')
        return response
    action_daily_activities_pdf.short_description = pgettext_lazy(
        'Activity',
        'Daily activities (PDF)')

    def get_monthly_activities(self, request, queryset):
        queryset = queryset.order_by('date')
        # Get minimum and maximum dates
        range_dates = queryset.aggregate(models.Min('date'),
                                         models.Max('date'))
        date_min = range_dates['date__min']
        date_max = range_dates['date__max']
        results = {}
        totals = {}
        details = {}
        structures = []
        for day in range(date_min.toordinal(), date_max.toordinal() + 1):
            results[str(day)] = defaultdict(int)
            totals[str(day)] = 0
            details[str(day)] = []
        # Add grand totals
        grand_totals = defaultdict(int)
        # Get every used service
        ServiceNM = collections.namedtuple('Service', 'id name')
        services = [ServiceNM(service[0], service[1])
                    for service in activity_room.ActivityRoom.objects.filter(
                    activity_id__in=queryset.values_list('id')).values_list(
                    'service_id', 'service__name').order_by(
                    'service_id').distinct()]
        # Cycle each unique date
        for activity in queryset:
            day = activity.date.toordinal()
            # Get totals for each activity
            for total in activity_room.ActivityRoom.objects.filter(
                    activity=activity).values(
                    'service_id', 'room__building__structure_id',
                    'description').annotate(
                    count=models.Count('service_id')).order_by('service_id'):
                structures.append(total['room__building__structure_id'])
                # Add description, if any
                if total['description']:
                    details[str(day)].append(total['description'])
                results[str(day)][total['service_id']] += total['count']
                totals[str(day)] += total['count']
                grand_totals[total['service_id']] += total['count']
                grand_totals['totals'] += total['count']
        # Prepare structures
        StructureNM = collections.namedtuple('Service', 'name company')
        structures = [StructureNM(structure.name, structure.company.name)
                      for structure
                      in Structure.objects.filter(id__in=structures).all()]
        # Export data
        context = dict(
            # Include common variables for rendering the admin template
            self.admin_site.each_context(request),
            results=results,
            totals=totals,
            grand_totals=grand_totals,
            details=dict([(item[0], '\n'.join(item[1]))
                         for item in details.items()]),
            structures=structures,
            # Ordinals are the numeric days, used for keys
            ordinals=range(date_min.toordinal(), date_max.toordinal() + 1),
            # Dates are the date objects
            dates=dict([(str(day), datetime.date.fromordinal(day))
                        for day in range(date_min.toordinal(),
                                         date_max.toordinal() + 1)]),
            # Services list
            services=services
        )
        return context

    def action_monthly_activities_html(self, request, queryset):
        context = self.get_monthly_activities(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        # Format dates
        if context.get('format_date'):
            context['dates'] = dict([(key,
                                      date.strftime(context['format_date']))
                                     for key, date
                                     in context['dates'].items()])
        response = TemplateResponse(request,
                                    'work/activities_monthly/admin.html',
                                    context)
        return response
    action_monthly_activities_html.short_description = (
        'Monthly activities (HTML)')

    def action_monthly_activities_pdf(self, request, queryset):
        context = self.get_monthly_activities(request, queryset)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        # Format dates
        if context.get('format_date'):
            context['dates'] = dict([(key,
                                      date.strftime(context['format_date']))
                                     for key, date
                                     in context['dates'].items()])
        response = xhtml2pdf_render_from_template_response(
            response=TemplateResponse(request,
                                      'work/activities_monthly/pdf.html',
                                      context),
            filename='')
        return response
    action_monthly_activities_pdf.short_description = pgettext_lazy(
        'Activity',
        'Monthly activities (PDF)')


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
        return results
