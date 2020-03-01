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

from .bed_type import BedType, BedTypeAdmin                       # noqa: F401
from .brand import Brand, BrandAdmin                              # noqa: F401
from .building import Building, BuildingAdmin                     # noqa: F401
from .company import Company, CompanyAdmin                        # noqa: F401
from .equipment import Equipment, EquipmentAdmin                  # noqa: F401
from .equipment_item import EquipmentItem, EquipmentItemAdmin     # noqa: F401
from .equipment_type import EquipmentType, EquipmentTypeAdmin     # noqa: F401
from .room import Room, RoomAdmin                                 # noqa: F401
from .room_type import RoomType, RoomTypeAdmin                    # noqa: F401
from .service import Service, ServiceAdmin                        # noqa: F401
from .service_extra import ServiceExtra, ServiceExtraAdmin        # noqa: F401
from .service_type import ServiceType, ServiceTypeAdmin           # noqa: F401
from .structure import Structure, StructureAdmin                  # noqa: F401
