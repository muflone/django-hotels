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

from django.views.generic import TemplateView

from ..models import HomeSection

from project import VERSION


class GenericView(TemplateView):
    """Generic view"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = VERSION
        context['request_path'] = self.request.path
        context['header_sections'] = HomeSection.objects.filter(
            header_order__gt=0).order_by('header_order')
        return context
