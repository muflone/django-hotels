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

import sys

import django

import json_views

import project

from .api_base import APIv1BaseView


class APIv1VersionsView(APIv1BaseView):
    login_with_tablet_id = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = project.VERSION
        context['python version'] = sys.version
        context['python version info'] = sys.version_info
        context['django version'] = django.__version__
        context['django version info'] = django.VERSION
        context['json_views version'] = json_views.__version__
        context['json_views version info'] = json_views.__version_info__
        # Add closing status (to check for transmission errors)
        self.add_status(context)
        return context
