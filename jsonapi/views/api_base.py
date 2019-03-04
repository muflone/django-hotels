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

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

import json_views.views

from work.models import Tablet


class APIBaseView(json_views.views.JSONDataView):
    login_with_tablet_id = True
    tablet = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.login_with_tablet_id:
            try:
                self.tablet = Tablet.objects.get(id=kwargs['tablet_id'])
                # Raise error 403 for invalid password
                if not self.tablet.check_password(password=kwargs['password']):
                    raise PermissionDenied
            except Tablet.DoesNotExist:
                # Raise error 404 for invalid tablet id
                self.tablet = None
                raise ObjectDoesNotExist('Tablet {TABLET_ID} not found'.format(
                    TABLET_ID=kwargs['tablet_id']))
        # Remove password from context
        context.pop('password', None)

        return context

    def add_status(self, context):
        """Add context status response with OK"""
        context['status'] = 'OK'
