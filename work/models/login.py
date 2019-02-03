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

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models

from utility.models import BaseModel, BaseModelAdmin


class Login(BaseModel, User):
    """User with app settings"""
    employee = models.OneToOneField('Employee',
                                    on_delete=models.PROTECT)

    class Meta:
        # Define the database table
        db_table = 'work_logins'

    def __str__(self):
        return '{FIRST_NAME} {LAST_NAME}'.format(
            FIRST_NAME=self.employee.first_name,
            LAST_NAME=self.employee.last_name)


class LoginAdmin(BaseModelAdmin, UserAdmin):
    model = Login
    change_form_template = 'work/admin_login_change.html'
    # Fieldset for login edit
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee', 'username'),
        }),
    )
    # Fieldset for login add
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee', 'username', 'password1', 'password2'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Protect fields after creation"""
        if obj:
            return ('employee', 'username')
        else:
            return ()

    def save_model(self, request, obj, form, change):
        obj.first_name = obj.employee.first_name
        obj.last_name = obj.employee.last_name
        obj.email = obj.employee.email
        # Save model data
        super().save_model(request, obj, form, change)
