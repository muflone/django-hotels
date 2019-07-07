##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2019 Fabio Castelli
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

from .models import (Activity, ActivityAdmin,
                     ActivityInLinesProxy, ActivityInLinesAdmin,
                     ActivityRoom, ActivityRoomAdmin,
                     Contract, ContractAdmin,
                     ContractType, ContractTypeAdmin,
                     Employee, EmployeeAdmin,
                     JobType, JobTypeAdmin,
                     Login, LoginAdmin,
                     Tablet, TabletAdmin,
                     Timestamp, TimestampAdmin,
                     TimestampDirection, TimestampDirectionAdmin)


# Register your models here.
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityInLinesProxy, ActivityInLinesAdmin)
admin.site.register(ActivityRoom, ActivityRoomAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractType, ContractTypeAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(JobType, JobTypeAdmin)
admin.site.register(Login, LoginAdmin)
admin.site.register(Tablet, TabletAdmin)
admin.site.register(Timestamp, TimestampAdmin)
admin.site.register(TimestampDirection, TimestampDirectionAdmin)
