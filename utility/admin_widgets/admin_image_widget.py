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

import os.path

from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import mark_safe


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs, width, height):
        result = ''
        if value and hasattr(value, 'url') and not value.url.startswith(
                os.path.join(settings.MEDIA_URL, 'standard%3A')):
            result = ('<a href="{URL}" target="_blank">'
                      '<img src="{URL}" width="{WIDTH}" height="{HEIGHT}">'
                      '</a>'.format(URL=value.url, WIDTH=width, HEIGHT=height))
        # Call super class and return results
        result += AdminFileWidget.render(self, name, value, attrs)
        return mark_safe(result)


# noinspection PyPep8Naming
class AdminImageWidget_64x64(AdminImageWidget):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs, 64, 64)


# noinspection PyPep8Naming
class AdminImageWidget_128x128(AdminImageWidget):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs, 128, 128)


# noinspection PyPep8Naming
class AdminImageWidget_256x256(AdminImageWidget):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs, 256, 256)
