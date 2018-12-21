##
#     Project: Django Milazzo Inn
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
from django.contrib.auth.views import LogoutView

from .views import TimeStampLoginView


urlpatterns = []
# Login page
urlpatterns.append(url(r'^login/$', TimeStampLoginView.as_view(
    template_name='login/login.html',
    extra_context={'next': '.',
                   'page_title': ('Login to register your presence', )}),
    name='work/page_login'))
# Logout page
urlpatterns.append(url(r'^logout/$', LogoutView.as_view(
    template_name='login/logout.html',
    extra_context={'next_page': 'work/page_login',
                   'page_title': ('Logout', )}),
    name='work/page_logout'))