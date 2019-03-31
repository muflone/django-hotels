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

from django.conf.urls import url

from . import views


urlpatterns = []

# Version page
urlpatterns.append(url(r'^v1/versions/$',
                       views.APIv1VersionsView.as_view(),
                       name='api/v1/versions'))
# Status page
urlpatterns.append(url(r'^v1/status/$',
                       views.APIv1StatusView.as_view(),
                       name='api/v1/status'))
# Status page
urlpatterns.append(url(r'^v1/dates/$',
                       views.APIv1DatesView.as_view(),
                       name='api/v1/dates'))
# Get page
urlpatterns.append(url(r'^v1/get/'
                       '(?P<tablet_id>\d+)/'
                       '(?P<password>\d+)/$',
                       views.APIv1GetView.as_view(),
                       name='api/v1/get'))
# Put timestamp page
urlpatterns.append(url(r'^v1/put/timestamp/'
                       '(?P<tablet_id>\d+)/'
                       '(?P<password>\d+)/'
                       '(?P<contract_id>\d+)/'
                       '(?P<direction>\w+)/'
                       '(?P<datetime>\d+)/'
                       '(?P<description>.*)/$',
                       views.APIv1PutTimestamp.as_view(),
                       name='api/v1/put/timestamp'))
