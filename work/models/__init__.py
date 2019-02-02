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

from .activity import Activity, ActivityAdmin                     # noqa: F401
from .activity import ActivityInLinesProxy, ActivityInLinesAdmin  # noqa: F401
from .activity_room import ActivityRoom, ActivityRoomAdmin        # noqa: F401
from .contract import Contract, ContractAdmin                     # noqa: F401
from .contract_type import ContractType, ContractTypeAdmin        # noqa: F401
from .employee import Employee, EmployeeAdmin                     # noqa: F401
from .job_type import JobType, JobTypeAdmin                       # noqa: F401
from .login import Login, LoginAdmin                              # noqa: F401
from .tablet import Tablet, TabletAdmin                           # noqa: F401
from .timestamp import Timestamp, TimestampAdmin                  # noqa: F401
from .timestamp_direction import (TimestampDirection,             # noqa: F401
                                  TimestampDirectionAdmin)        # noqa: F401
