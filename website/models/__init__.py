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

from .admin_option import AdminOption, AdminOptionAdmin           # noqa: F401
from .home_section import HomeSection, HomeSectionAdmin           # noqa: F401

# Keep all the models with a field model always at the last imports
# to first include all the previous models in get_admin_models
from .admin_export_csv_map import (AdminExportCSVMap,             # noqa: F401
                                   AdminExportCSVMapAdmin)        # noqa: F401
from .admin_list_display import (AdminListDisplay,                # noqa: F401
                                 AdminListDisplayAdmin)           # noqa: F401
from .admin_list_display_link import (AdminListDisplayLink,       # noqa: F401
                                      AdminListDisplayLinkAdmin)  # noqa: F401
from .admin_list_filter import (AdminListFilter,                  # noqa: F401
                                AdminListFilterAdmin)             # noqa: F401
from .admin_searchable import (AdminSearchable,                   # noqa: F401
                               AdminSearchableAdmin)              # noqa: F401
