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
import urllib.parse

from work.models import Activity
from work.models import ActivityRoom

from .api_base import APIv1BaseView


class APIv1PutActivity(APIv1BaseView):
    login_with_tablet_id = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'description' not in context:
            context['description'] = ''

        activity_date = (datetime.datetime.fromtimestamp(
            int(context['datetime'])).replace(hour=0,
                                              minute=0,
                                              second=0,
                                              microsecond=0))
        activity_query = Activity.objects.filter(
            contract_id=int(context['contract_id']),
            date=activity_date)
        if activity_query:
            # Look for existing activity
            activity = activity_query[0]
        else:
            # No existing activity, create a new one
            activity = Activity.objects.create(
                contract_id=int(context['contract_id']),
                date=activity_date)
        # Add Activity room to activity
        activity_query = ActivityRoom.objects.filter(
            activity_id=activity.pk,
            room_id=int(context['room_id']),
            service_id=int(context['service_id']))
        if activity_query:
            activity = activity_query[0]
            if activity.service_qty != int(context['service_qty']):
                # Existing activity but with a different quantity
                context['status'] = 'QUANTITY'
            elif activity.description != urllib.parse.unquote_plus(
                    context['description'].replace('\\n', '\n')):
                # Existing activity but with a different description
                context['status'] = 'DESCRIPTION'
            else:
                # Existing matching activity
                context['status'] = 'EXISTING'
        else:
            # No existing timestamp
            activity = ActivityRoom.objects.create(
                activity_id=activity.pk,
                room_id=int(context['room_id']),
                service_id=int(context['service_id']),
                service_qty=int(context['service_qty']),
                description=urllib.parse.unquote_plus(
                    context['description'].replace('\\n', '\n')))
            # Add closing status (to check for transmission errors)
            self.add_status(context)
        # Return timestamp id
        context['activity_id'] = activity.pk
        return context
