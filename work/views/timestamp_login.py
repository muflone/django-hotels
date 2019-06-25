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
import sys

from django.contrib import auth
from django.contrib.auth.views import LoginView

from utility.misc import get_admin_options
from ..forms import TimeStampLoginForm
from ..models import Login, Timestamp, TimestampDirection

from website.views import GenericView


class TimeStampLoginView(LoginView, GenericView):

    form_class = TimeStampLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add report preferences from AdminOptions
        context.update(get_admin_options(self.__class__.__name__,
                                         sys._getframe().f_code.co_name))
        # Split last_logins_columns in multiple values
        last_logins_columns = context['last_logins_columns']
        context['last_logins_columns'] = ([column.strip()
                                           for column
                                           in last_logins_columns.split(',')]
                                          if last_logins_columns
                                          else None)
        if self.request.user.is_authenticated:
            obj_login = Login.objects.get(username=self.request.user)
            active_contract = obj_login.employee.get_active_contract()
            context['page_title'] = ('Welcome {EMPLOYEE}'.format(
                EMPLOYEE=obj_login.employee), )
            context['last_logins'] = Timestamp.objects.filter(
                contract=active_contract).order_by(
                '-date', '-time')[:int(context['last_logins_count'])]
        else:
            context['page_title'] = ('Login to register your presence', )
        return context

    def form_valid(self, form):
        if Login.objects.filter(username=form.get_user()):
            auth.login(self.request, form.get_user())
            obj_login = Login.objects.get(username=self.request.user)
            active_contract = obj_login.employee.get_active_contract()
            if active_contract:
                access_type = form.cleaned_data['access_type']
                Timestamp.objects.create(
                    contract=active_contract,
                    direction=(TimestampDirection.get_exit_direction()
                               if access_type == 'exit'
                               else TimestampDirection.get_enter_direction()),
                    date=datetime.date.today(),
                    time=datetime.datetime.now().replace(microsecond=0),
                    description=form.cleaned_data['description'])
                return super().form_valid(form)
