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

from django.views.generic import TemplateView

from ..models import HomeSection


class HomeView(TemplateView):
    """Home view"""
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['request_path'] = self.request.path
        context['home_section'] = HomeSection.objects.filter(name='Home')[0]
        context['header_sections'] = HomeSection.objects.filter(
            header_order__gt=0).order_by('header_order')
        context['home_sections'] = HomeSection.objects.filter(
            home_order__gt=0).order_by('home_order')
        context['page_title'] = context['home_section'].home_title,
        context['page_content'] = context['home_section'].description.replace(
            '\r', '').split('\n\n')
        return context
