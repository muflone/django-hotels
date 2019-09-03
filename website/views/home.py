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

from . import GenericView

from ..models import HomeSection


class HomeView(GenericView):
    """Home view"""
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_section'] = HomeSection.objects.filter(name='Home')[0]
        context['home_sections'] = HomeSection.objects.filter(
            home_order__gt=0).order_by('home_order')
        context['page_title'] = context['home_section'].home_title,
        context['page_content'] = context['home_section'].description.replace(
            '\r', '').split('\n\n')
        return context
