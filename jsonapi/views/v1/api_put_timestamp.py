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

from work.models import Timestamp
from work.models import TimestampDirection

from .api_base import APIv1BaseView


class APIv1PutTimestamp(APIv1BaseView):
    login_with_tablet_id = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        timestamp_query = Timestamp.objects.filter(
            contract_id=int(context['contract_id']),
            direction_id=int(context['direction_id']),
            date=datetime.datetime.fromtimestamp(int(context['datetime'])),
            time=datetime.datetime.fromtimestamp(int(context['datetime'])))
        if timestamp_query:
            # Whether the timestamp already exists reply with an EXISTING status
            timestamp = timestamp_query[0]
            context['status'] = 'EXISTING'
        else:
            # No existing timestamp
            timestamp = Timestamp.objects.create(
                contract_id=int(context['contract_id']),
                direction_id=int(context['direction_id']),
                date=datetime.datetime.fromtimestamp(int(context['datetime'])),
                time=datetime.datetime.fromtimestamp(int(context['datetime'])),
                description=context['description'])
            # Add closing status (to check for transmission errors)
            self.add_status(context)
        # Return timestamp id
        context['timestamp_id'] = timestamp.pk
        return context
