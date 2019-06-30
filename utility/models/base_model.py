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

from django.contrib import admin
from django.db import models

from utility.admin_mixins import ExportCSVMixin


class BaseModel(models.Model):

    def __init__(self, *args, **kwargs):
        """Base model for each other model in the application"""
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True


class BaseModelAdmin(admin.ModelAdmin, ExportCSVMixin):

    def __init__(self, model, admin_site):
        """Base Admin model for each other model in the application"""
        super().__init__(model, admin_site)
        # If ModelAdmin ordering is missing apply the ordering of the model
        if not self.ordering:
            self.ordering = model._meta.ordering
        # Add Export rows to CSV action
        ExportCSVMixin.__init__(self)
