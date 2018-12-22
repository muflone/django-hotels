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

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Login


class TimeStampLoginForm(AuthenticationForm):
    access_type = forms.CharField(label='Login type', max_length=10)
    description = forms.CharField(label='Description or annotations',
                                  widget=forms.Textarea,
                                  required=False)

    def confirm_login_allowed(self, user):
        if Login.objects.filter(username=user):
            obj_login = Login.objects.get(username=user)
            active_contract = obj_login.employee.get_active_contract()
            if not active_contract:
                raise forms.ValidationError(
                    'Missing contract for employee {EMPLOYEE}.'.format(
                    EMPLOYEE=obj_login.employee),
                    code='missing_contract')
        else:
            raise forms.ValidationError(
                'Username {USERNAME} invalid.'.format(
                USERNAME=user),
                code='invalid_login')
