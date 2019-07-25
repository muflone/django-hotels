##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2019 Fabio Castelli
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
import sys
import urllib.parse

from hotels.models import Room

from utility.misc import get_admin_options

from work.models import Activity
from work.models import ActivityRoom

from .api_base import APIv1BaseView


class APIv1PutExtra(APIv1BaseView):
    login_with_tablet_id = False

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
        # Add Activity extra to activity
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        # The building ID used for the extras
        extra_building_id = int(context['extras_building_id'])
        activity = ActivityRoom.objects.create(
            activity_id=activity.pk,
            # The Room ID to use is the nth from the building extra_building_id
            # See AdminOption extras_building_id
            room_id=Room.objects.filter(building=extra_building_id)
                [int(context['room_id']) - 1].pk,
            service_id=int(context['extras_service_id']),
            service_qty=int(context['service_qty']),
            description=urllib.parse.unquote_plus(
                context['description'].replace('\\n', '\n')))
        # Add closing status (to check for transmission errors)
        self.add_status(context)
        # Return timestamp id
        context['activity_id'] = activity.pk
        return context
