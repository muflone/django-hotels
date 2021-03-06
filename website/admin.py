##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2020 Fabio Castelli
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

from collections import OrderedDict

from django.contrib import admin
from django.db.utils import OperationalError


from .models import (AdminExportCSVMap, AdminExportCSVMapAdmin,
                     AdminListDisplay, AdminListDisplayAdmin,
                     AdminListDisplayLink, AdminListDisplayLinkAdmin,
                     AdminListFilter, AdminListFilterAdmin,
                     AdminOption, AdminOptionAdmin,
                     AdminSearchable, AdminSearchableAdmin,
                     HomeSection, HomeSectionAdmin)

from utility.misc import get_admin_models, get_class_from_module


# Register your models here.
admin.site.register(AdminExportCSVMap, AdminExportCSVMapAdmin)
admin.site.register(AdminListDisplay, AdminListDisplayAdmin)
admin.site.register(AdminListDisplayLink, AdminListDisplayLinkAdmin)
admin.site.register(AdminListFilter, AdminListFilterAdmin)
admin.site.register(AdminOption, AdminOptionAdmin)
admin.site.register(AdminSearchable, AdminSearchableAdmin)
admin.site.register(HomeSection, HomeSectionAdmin)

admin_models = get_admin_models()

# Customize Administration
try:
    for option in AdminOption.objects.filter(section='Django Admin',
                                             enabled=True):
        if option.name == 'site_header':
            admin.site.site_header = option.value
        elif option.name == 'site_title':
            admin.site.site_title = option.value
        elif option.name == 'index_title':
            admin.site.index_title = option.value
except OperationalError:
    # If the model AdminOption doesn't yet exist skip the customization
    pass

# Customize searchables
try:
    for item in AdminSearchable.objects.filter(use_select2=True):
        admin_models[item.ref_model].search_fields = (item.ref_field, )
        admin_models[item.model].autocomplete_fields += (item.field, )
except OperationalError:
    # If the model AdminSearchable doesn't yet exist skip the customization
    pass

# Customize list_display
try:
    # Clear or initialize the model list_display
    for model_name in admin_models:
        admin_models[model_name].list_display = []
    # Add the fields to model list_display
    for item in AdminListDisplay.objects.filter(enabled=True).order_by(
            'model', 'order'):
        # Include only existing models
        if item.model in admin_models:
            admin_models[item.model].list_display.append(item.field)
except OperationalError:
    # If the model AdminListDisplay doesn't yet exist skip the customization
    pass

# Customize list_display_links
try:
    # Clear or initialize the model list_display_links
    for model_name in admin_models:
        admin_models[model_name].list_display_links = []
    # Add the fields to model list_display_links
    for item in AdminListDisplayLink.objects.filter(enabled=True).order_by(
            'model', 'order'):
        admin_models[item.model].list_display_links.append(item.field)
except OperationalError:
    # If the model AdminListDisplayLink doesn't yet exist skip the
    # customization
    pass

# Customize list_filter
try:
    # Clear or initialize the model list_filter
    for model_name in admin_models:
        admin_models[model_name].list_filter = []
    # Add the fields to model list_display_links
    for item in AdminListFilter.objects.filter(enabled=True).order_by(
            'model', 'order'):
        if '|' in item.field:
            # The filter contains multiple fields
            new_fields = []
            fields = item.field.split('|')
            for field in fields:
                if '.' in field:
                    # The filter contain a module.class field
                    field = get_class_from_module(field)
                new_fields.append(field)
        elif '.' in item.field:
            # The filter contain a module.class field
            new_fields = get_class_from_module(item.field)
        else:
            # The filter is a string filter
            new_fields = item.field
        # Include only existing models
        if item.model in admin_models:
            admin_models[item.model].list_filter.append(new_fields)
except OperationalError:
    # If the model AdminListFilter doesn't yet exist skip the customization
    pass

# Customize export_csv_fields_map
try:
    # Clear or initialize the model export_csv_fields_map
    for model_name in admin_models:
        admin_models[model_name].export_csv_fields_map = OrderedDict()
    # Add the fields to model export_csv_fields_map
    for item in AdminExportCSVMap.objects.filter(enabled=True).order_by(
            'model', 'order', 'title'):
        # Include only existing models
        if item.model in admin_models:
            admin_models[item.model].export_csv_fields_map[item.title] = (
                item.field)
except OperationalError:
    # If the model AdminExportCSVMap doesn't yet exist skip the
    # customization
    pass

# Final checks on every model
for model_name in admin_models:
    # Add missing fields from model list_display_links to model list_display
    for item in admin_models[model_name].list_display_links:
        if item not in admin_models[model_name].list_display:
            admin_models[model_name].list_display.append(item)
    # For empty model list_display add the standard __str__ field
    if not admin_models[model_name].list_display:
        admin_models[model_name].list_display.append('__str__')
