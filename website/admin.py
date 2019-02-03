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
from django.db.utils import OperationalError


from .models import (AdminSearchable, AdminSearchableAdmin,
                     AdminSection, AdminSectionAdmin,
                     HomeSection, HomeSectionAdmin)

from utility.misc import get_admin_models


# Register your models here.
admin.site.register(AdminSearchable, AdminSearchableAdmin)
admin.site.register(AdminSection, AdminSectionAdmin)
admin.site.register(HomeSection, HomeSectionAdmin)

# Customize Administration
try:
    for section in AdminSection.objects.all():
        if section.name == 'site_header':
            admin.site.site_header = section.description
        elif section.name == 'site_title':
            admin.site.site_title = section.description
        elif section.name == 'index_title':
            admin.site.index_title = section.description
except OperationalError:
    # If the model AdminSection doesn't yet exist skip the customization
    pass

# Customize models
admin_models = get_admin_models()
# Customize searchables
try:
    for item in AdminSearchable.objects.filter(use_select2=True):
        admin_models[item.ref_model].search_fields = (item.ref_field, )
        admin_models[item.model].autocomplete_fields += (item.field, )
except OperationalError:
    # If the model AdminSearchable doesn't yet exist skip the customization
    pass
