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

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.forms.widgets import MediaDefiningClass


def get_admin_models():
    """Get all the ModelAdmin in every loaded application"""
    admin_models = {}
    for application in apps.app_configs.keys():
        application_module = apps.app_configs[application]
        application_module.import_models()
        for module_name in dir(application_module.models_module):
            obj = getattr(application_module.models_module, module_name)
            if (issubclass(obj.__class__, MediaDefiningClass) and
                    issubclass(obj, admin.options.BaseModelAdmin) and
                    # Avoid to list the BaseModelAdmin class
                    obj.__name__ not in 'BaseModelAdmin'):
                admin_models[obj.__name__] = obj
    # Add dummy models from ADMIN_MODELS_REFERENCING_MODELS_WITH_CHOICES
    for obj in settings.ADMIN_MODELS_REFERENCING_MODELS_WITH_CHOICES:
        if obj not in admin_models:
            admin_models[obj] = None
    return admin_models
