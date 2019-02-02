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

from hotels.models import Room

from .api_base import APIBaseView


class APIBuildingsView(APIBaseView):
    login_with_tablet_id = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        structures = {}
        # List all buildings and structures
        for obj_building in self.tablet.buildings.all():
            obj_structure = obj_building.structure
            if obj_structure.name not in structures:
                buildings = []
                structures[obj_structure.name] = {
                    'name': obj_structure.name,
                    'description': obj_structure.description,
                    'buildings': buildings}
            else:
                structure = structures[obj_building.structure.name]
                buildings = structure['buildings']

            rooms = Room.objects.filter(building_id=obj_building.id).values(
                'id', 'name', 'description', 'room_type__description')
            buildings.append({'id': obj_building.id,
                              'name': obj_building.name,
                              'description': obj_building.description,
                              'rooms': rooms})
        context['structures'] = structures
        return context
