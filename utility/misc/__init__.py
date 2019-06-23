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

from .admin_models import get_admin_models                        # noqa: F401
from .admin_options import get_admin_options                      # noqa: F401
from .dates import month_start, month_end                         # noqa: F401
from .get_class_from_module import get_class_from_module          # noqa: F401
from .get_full_host import get_full_host                          # noqa: F401
from .qrcode_image import QRCodeImage                             # noqa: F401
from .reverse_with_query import reverse_with_query                # noqa: F401
from .uri import URI                                              # noqa: F401
from .xhtml2pdf import (xhtml2pdf_link_callback,                  # noqa: F401
                        xhtml2pdf_render_from_html,               # noqa: F401
                        xhtml2pdf_render_from_template_response)  # noqa: F401
