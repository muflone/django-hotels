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

from django.contrib import admin

from .models import (BedType, BedTypeAdmin,
                     Brand, BrandAdmin,
                     Building, BuildingAdmin,
                     Company, CompanyAdmin,
                     Equipment, EquipmentAdmin,
                     EquipmentItem, EquipmentItemAdmin,
                     EquipmentType, EquipmentTypeAdmin,
                     Room, RoomAdmin,
                     RoomType, RoomTypeAdmin,
                     Service, ServiceAdmin,
                     ServiceExtra, ServiceExtraAdmin,
                     ServiceType, ServiceTypeAdmin,
                     Structure, StructureAdmin)


# Register your models here.
admin.site.register(BedType, BedTypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentItem, EquipmentItemAdmin)
admin.site.register(EquipmentType, EquipmentTypeAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceExtra, ServiceExtraAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Structure, StructureAdmin)
