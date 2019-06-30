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
import json

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

import json_views.views

from jsonapi.models import ApiLog

from work.models import Tablet


class APIv1BaseView(json_views.views.JSONDataView):
    login_with_tablet_id = True
    tablet = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.add_log(message_level=0,
                     tablet_id=kwargs.get('tablet_id', 0),
                     extra=None)
        if self.login_with_tablet_id:
            try:
                self.tablet = Tablet.objects.get(id=kwargs['tablet_id'])
                if not self.tablet.check_password(password=kwargs['password']):
                    # Raise error 403 for invalid password
                    self.add_log(message_level=20,
                                 tablet_id=kwargs.get('tablet_id', 0),
                                 extra='Permission denied for invalid password'
                                 )
                    raise PermissionDenied
                elif not self.tablet.status:
                    # Raise error 403 for status disabled
                    self.add_log(message_level=20,
                                 tablet_id=kwargs.get('tablet_id', 0),
                                 extra='Permission denied for disabled status')
                    raise PermissionDenied
            except Tablet.DoesNotExist:
                # Raise error 404 for invalid tablet id
                self.add_log(message_level=20,
                             tablet_id=kwargs.get('tablet_id', 0),
                             extra='Tablet does not exist')
                self.tablet = None
                raise ObjectDoesNotExist('Tablet {TABLET_ID} not found'.format(
                    TABLET_ID=kwargs['tablet_id']))
        # Remove password from context
        context.pop('password', None)

        return context

    def add_status(self, context):
        """Add context status response with OK"""
        context['status'] = 'OK'

    def add_log(self, message_level, tablet_id, extra):
        """Add an entry to the ApiLog"""
        ApiLog.objects.create(
            date=datetime.date.today(),
            time=datetime.datetime.now().replace(microsecond=0),
            message_level=message_level,
            method=self.request.method,
            path=self.request.path,
            raw_uri=self.request.get_raw_uri(),
            url_name=self.request.resolver_match.url_name,
            func_name=self.request.resolver_match.func.__name__,
            remote_addr=self.request.META.get('REMOTE_ADDR', ''),
            forwarded_for=self.request.META.get('HTTP_X_FORWARDED_FOR', ''),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            client_agent=self.request.META.get('HTTP_CLIENT_AGENT', ''),
            client_version=self.request.META.get('HTTP_CLIENT_VERSION', ''),
            user=self.request.user,
            tablet_id=tablet_id,
            kwargs=self.json_prettify(self.request.resolver_match.kwargs),
            args=self.json_prettify(self.request.resolver_match.args),
            extra=extra if extra is not None else '',
            api_version=1)

    def json_prettify(self, arguments):
        """Format the arguments in JSON formatted style"""
        return (json.dumps(arguments, sort_keys=False, indent=2)
                if arguments else '')
