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

import django.urls as urls

from . import views

from utility.converters import (IsoDateStrConverter,
                                IsoTimeStrConverter,
                                OTPKeyConverter)


urls.register_converter(IsoDateStrConverter, IsoDateStrConverter.name)
urls.register_converter(IsoTimeStrConverter, IsoTimeStrConverter.name)
urls.register_converter(OTPKeyConverter, OTPKeyConverter.name)

urlpatterns = []

# Version page
urlpatterns.append(urls.path('v1/versions/',
                             views.APIv1VersionsView.as_view(),
                             name='api/v1/versions'))
urlpatterns.append(urls.path('v1/versions/'
                             '<int:tablet_id>/',
                             views.APIv1VersionsView.as_view(),
                             name='api/v1/versions'))
# Status page
urlpatterns.append(urls.path('v1/status/',
                             views.APIv1StatusView.as_view(),
                             name='api/v1/status'))
urlpatterns.append(urls.path('v1/status/'
                             '<int:tablet_id>/',
                             views.APIv1StatusView.as_view(),
                             name='api/v1/status'))
# Usage page
urlpatterns.append(urls.path('v1/usage/',
                             views.APIv1UsageView.as_view(),
                             name='api/v1/usage'))
urlpatterns.append(urls.path('v1/usage/'
                             '<int:tablet_id>/',
                             views.APIv1UsageView.as_view(),
                             name='api/v1/usage'))
# Dates page
urlpatterns.append(urls.path('v1/dates/',
                             views.APIv1DatesView.as_view(),
                             name='api/v1/dates'))
urlpatterns.append(urls.path('v1/dates/'
                             '<int:tablet_id>/'
                             '<isodate_str:tablet_date>/'
                             '<isotime_str:tablet_time>/'
                             '<str:tablet_timezone>/'
                             '<str:tablet_timezone_id>/',
                             views.APIv1DatesView.as_view(),
                             name='api/v1/dates'))
# Get page
urlpatterns.append(urls.path('v1/get/'
                             '<int:tablet_id>/'
                             '<otpkey:password>/',
                             views.APIv1GetView.as_view(),
                             name='api/v1/get'))
# Put activity page
urlpatterns.append(urls.path('v1/put/activity/'
                             '<int:tablet_id>/'
                             '<otpkey:password>/'
                             '<int:contract_id>/'
                             '<int:room_id>/'
                             '<int:service_id>/'
                             '<int:service_qty>/'
                             '<int:datetime>/'
                             '<str:description>/',
                             views.APIv1PutActivity.as_view(),
                             name='api/v1/put/activity'))
urlpatterns.append(urls.path('v1/put/activity/'
                             '<int:tablet_id>/'
                             '<otpkey:password>/'
                             '<int:contract_id>/'
                             '<int:room_id>/'
                             '<int:service_id>/'
                             '<int:service_qty>/'
                             '<int:datetime>/'
                             '/',
                             views.APIv1PutActivity.as_view(),
                             name='api/v1/put/activity'))
# Some web servers (Python Anywhere) don't handle well URLs with two ending
# slashes: two consecutive slashes are interpreted as a single slash
urlpatterns.append(urls.path('v1/put/activity/'
                             '<int:tablet_id>/'
                             '<otpkey:password>/'
                             '<int:contract_id>/'
                             '<int:room_id>/'
                             '<int:service_id>/'
                             '<int:service_qty>/'
                             '<int:datetime>/',
                             views.APIv1PutActivity.as_view(),
                             name='api/v1/put/activity'))
# Put timestamp page
urlpatterns.append(urls.path('v1/put/timestamp/'
                             '<int:tablet_id>/'
                             '<otpkey:password>/'
                             '<int:contract_id>/'
                             '<int:direction_id>/'
                             '<int:datetime>/'
                             '<str:description>/',
                             views.APIv1PutTimestamp.as_view(),
                             name='api/v1/put/timestamp'))
urlpatterns.append(urls.path('v1/put/timestamp/'
                             '<int:tablet_id>/'
                             '<otpkey:password>/'
                             '<int:contract_id>/'
                             '<int:direction_id>/'
                             '<int:datetime>/'
                             '/',
                             views.APIv1PutTimestamp.as_view(),
                             name='api/v1/put/timestamp'))
# Some web servers (Python Anywhere) don't handle well URLs with two ending
# slashes: two consecutive slashes are interpreted as a single slash
urlpatterns.append(urls.path('v1/put/timestamp/'
                             '<int:tablet_id>/'
                             '<otpkey:password>/'
                             '<int:contract_id>/'
                             '<int:direction_id>/'
                             '<int:datetime>/',
                             views.APIv1PutTimestamp.as_view(),
                             name='api/v1/put/timestamp'))
