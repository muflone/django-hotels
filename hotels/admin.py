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

from .models import (BedType, BedTypeAdmin,
                     Brand, BrandAdmin,
                     Building, BuildingAdmin,
                     Company, CompanyAdmin,
                     Equipment, EquipmentAdmin,
                     Room, RoomAdmin,
                     RoomType, RoomTypeAdmin,
                     Service, ServiceAdmin,
                     Structure, StructureAdmin)


# Register your models here.
admin.site.register(BedType, BedTypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Structure, StructureAdmin)
