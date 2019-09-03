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

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import pgettext_lazy

from . import models


class TimeStampLoginForm(AuthenticationForm):
    access_type = forms.CharField(label='Login type', max_length=10)
    description = forms.CharField(label='Description or annotations',
                                  widget=forms.Textarea,
                                  required=False)

    def confirm_login_allowed(self, user):
        if models.Login.objects.filter(username=user):
            obj_login = models.Login.objects.get(username=user)
            if not obj_login.contract.active():
                raise forms.ValidationError(
                    pgettext_lazy(
                        'TimeStampLoginForm',
                        'Missing contract for employee {EMPLOYEE}.').format(
                            EMPLOYEE=obj_login.contract.employee),
                    code='missing_contract')
        else:
            raise forms.ValidationError(
                pgettext_lazy(
                        'TimeStampLoginForm',
                        'Username {USERNAME} invalid.').format(USERNAME=user),
                code='invalid_login')


class ActivityRoomInlineForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }
