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

import datetime
import time

from django.contrib import auth
from django.contrib.auth.views import LoginView

from ..forms import TimeStampLoginForm
from ..models import Login, Timestamp

from website.views import GenericView


class TimeStampLoginView(LoginView, GenericView):

    form_class = TimeStampLoginForm

    def form_valid(self, form):
        if Login.objects.filter(username=form.get_user()):
            auth.login(self.request, form.get_user())
            obj_login = Login.objects.get(username=self.request.user)
            active_contract = obj_login.employee.get_active_contract()
            if active_contract:
                access_type = form.cleaned_data['access_type']
                Timestamp.objects.create(
                    contract=active_contract,
                    direction='>' if access_type == 'exit' else '<',
                    date=datetime.date.today(),
                    time=datetime.datetime.now(),
                    description=form.cleaned_data['description'])
                return super(self.__class__, self).form_valid(form)
