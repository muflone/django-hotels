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

from .continent import Continent, ContinentAdmin                  # noqa: F401
from .country import Country, CountryAdmin                        # noqa: F401
from .language import Language, LanguageAdmin                     # noqa: F401
from .location import Location, LocationAdmin                     # noqa: F401
from .position import Position, PositionAdmin                     # noqa: F401
from .region import Region, RegionAdmin                           # noqa: F401
from .region_alias import RegionAlias, RegionAliasAdmin           # noqa: F401
