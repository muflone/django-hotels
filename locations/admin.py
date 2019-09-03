##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2019 Fabio Castelli
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

from .models import (Continent, ContinentAdmin,
                     Country, CountryAdmin,
                     Language, LanguageAdmin,
                     Location, LocationAdmin,
                     Position, PositionAdmin,
                     Region, RegionAdmin,
                     RegionAlias, RegionAliasAdmin)


# Register your models here.
admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(RegionAlias, RegionAliasAdmin)
