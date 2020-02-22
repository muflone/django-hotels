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

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class Login(BaseModel, User):
    """User with app settings"""
    contract = models.ForeignKey('Contract',
                                 on_delete=models.PROTECT,
                                 verbose_name=pgettext_lazy('Login',
                                                            'contract'))
    default_structure = models.ForeignKey('hotels.Structure',
                                          default=0,
                                          on_delete=models.PROTECT,
                                          verbose_name=pgettext_lazy(
                                              'Login',
                                              'default structure'))

    class Meta:
        # Define the database table
        db_table = 'work_logins'
        verbose_name = pgettext_lazy('Login', 'Login')
        verbose_name_plural = pgettext_lazy('Login', 'Logins')

    def __str__(self):
        return '{FIRST_NAME} {LAST_NAME}'.format(
            FIRST_NAME=self.contract.employee.first_name,
            LAST_NAME=self.contract.employee.last_name)


class LoginAdmin(BaseModelAdmin, UserAdmin):
    model = Login
    change_form_template = 'work/admin_login_change.html'
    # Fieldset for login edit
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('contract', 'username', 'default_structure'),
        }),
    )
    # Fieldset for login add
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('contract', 'username', 'password1', 'password2',
                       'default_structure'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Protect fields after creation"""
        if obj:
            return 'contract', 'username'
        else:
            return ()

    def save_model(self, request, obj, form, change):
        obj.first_name = obj.contract.employee.first_name
        obj.last_name = obj.contract.employee.last_name
        obj.email = obj.contract.employee.email
        # Save model data
        super().save_model(request, obj, form, change)
