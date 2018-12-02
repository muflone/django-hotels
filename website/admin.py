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

from django.contrib import admin
from django.db.utils import OperationalError


from .models import (HomeSection, HomeSectionAdmin,
                     AdminOption, AdminOptionAdmin,
                     AdminSection, AdminSectionAdmin)

from locations.models import LocationAdmin

from hotels.models import BuildingAdmin, StructureAdmin


# Register your models here.
admin.site.register(HomeSection, HomeSectionAdmin)
admin.site.register(AdminOption, AdminOptionAdmin)
admin.site.register(AdminSection, AdminSectionAdmin)

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

# Customize options
try:
    for option in AdminOption.objects.all():
        if option.name == 'building.location.searchable' and option.value == '1':
            LocationAdmin.search_fields = ('name', )
            BuildingAdmin.autocomplete_fields = ('location', )
        elif option.name == 'hotel.location.searchable' and option.value == '1':
            LocationAdmin.search_fields = ('name', )
            StructureAdmin.autocomplete_fields = ('location', )
except OperationalError:
    # If the model AdminOption doesn't yet exist skip the customization
    pass
