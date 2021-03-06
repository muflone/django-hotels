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

from .api_dates import APIv1DatesView                             # noqa: F401
from .api_get import APIv1GetView                                 # noqa: F401
from .api_put_activity import APIv1PutActivity                    # noqa: F401
from .api_put_extra import APIv1PutExtra                          # noqa: F401
from .api_put_timestamp import APIv1PutTimestamp                  # noqa: F401
from .api_status import APIv1StatusView                           # noqa: F401
from .api_usage import APIv1UsageView                             # noqa: F401
from .api_versions import APIv1VersionsView                       # noqa: F401
