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

from work.models import Contract

from .api_base import APIv1BaseView


class APIv1GetView(APIv1BaseView):
    login_with_tablet_id = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # List all buildings and structures for the selected tablet
        structures = {}
        for obj_building in self.tablet.buildings.all():
            obj_structure = obj_building.structure
            if obj_structure.name not in structures:
                # Add new structure if doesn't exist
                obj_location = obj_structure.location
                obj_region = obj_location.region
                obj_country = obj_region.country
                structure = {'structure': {'id': obj_structure.id,
                                           'name': obj_structure.name
                                           },
                             'company': {'id': obj_structure.company.pk,
                                         'name': obj_structure.company.name
                                         },
                             'brand': {'id': obj_structure.brand.pk,
                                       'name': obj_structure.brand.name
                                       },
                             'location': {'id': obj_location.pk,
                                          'name': obj_location.name,
                                          'address': obj_structure.address,
                                          'region': {'id': obj_region.pk,
                                                     'name': obj_region.name
                                                     },
                                          'country': {'id': obj_country.pk,
                                                      'name': obj_country.name
                                                      },
                                          },
                             'buildings': []
                             }
                structures[obj_structure.name] = structure
            # Add buildings to the structure
            structure = structures[obj_building.structure.name]
            buildings = structure['buildings']
            obj_location = obj_building.location
            obj_region = obj_location.region
            obj_country = obj_region.country
            rooms = Room.objects.filter(building_id=obj_building.id).values(
                'id', 'name', 'description', 'room_type__name',
                'bed_type__name')
            building = {'building': {'id': obj_building.id,
                                     'name': obj_building.name,
                                     },
                        'location': {'id': obj_location.pk,
                                     'name': obj_location.name,
                                     'address': obj_structure.address,
                                     'region': {'id': obj_region.pk,
                                                'name': obj_region.name
                                                },
                                     'country': {'id': obj_country.pk,
                                                 'name': obj_country.name
                                                 },
                                     },
                        'rooms': [{'room': {'id': room['id'],
                                            'name': room['name']
                                            },
                                   'room_type': room['room_type__name'],
                                   'bed_type': room['bed_type__name'],
                                   }
                                  for room in rooms],
                        }
            buildings.append(building)
        context['structures'] = structures
        # List all the contracts for the selected tablet
        contracts = []
        for obj_contract in Contract.objects.filter(
                buildings__in=self.tablet.buildings.all()).distinct():
            obj_employee = obj_contract.employee
            obj_contract_type = obj_contract.contract_type
            obj_buildings = obj_contract.buildings
            contract = {'contract': {'id': obj_contract.pk,
                                     'guid': obj_contract.guid,
                                     'start': obj_contract.start_date,
                                     'end': obj_contract.start_date,
                                     'enabled': obj_contract.enabled,
                                     'active': obj_contract.active()
                                     },
                        'employee': {'id': obj_employee.pk,
                                     'first_name': obj_employee.first_name,
                                     'last_name': obj_employee.last_name,
                                     'genre': obj_employee.genre
                                     },
                        'company': {'id': obj_contract.company.pk,
                                    'name': obj_contract.company.name
                                    },
                        'type': {'id': obj_contract_type.pk,
                                 'name': obj_contract_type.name,
                                 'daily': obj_contract_type.daily_hours,
                                 'weekly': obj_contract_type.weekly_hours,
                                 },
                        'job': {'id': obj_contract.job_type.pk,
                                'name': obj_contract.job_type.name,
                                },
                        'buildings': [building_id['id']
                                      for building_id
                                      in obj_buildings.values('id')]
                        }
            contracts.append(contract)
        context['contracts'] = contracts
        # Add closing status (to check for transmission errors)
        self.add_status(context)
        return context
