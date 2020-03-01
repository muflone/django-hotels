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

import io
import os.path

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import pgettext_lazy

from xhtml2pdf import pisa


def xhtml2pdf_link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    static_url = settings.STATIC_URL
    static_root = settings.STATIC_ROOT
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT

    # convert URIs to absolute system paths
    if uri.startswith(media_url):
        path = os.path.join(media_root, uri.replace(media_url, ''))
    elif uri.startswith(static_url):
        path = os.path.join(static_root, uri.replace(static_url, ''))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(pgettext_lazy(
            'Utility',
            'media URI must start with {STATIC_URL} or {MEDIA_URL}').format(
                STATIC_URL=static_url,
                MEDIA_URL=media_url))
    return path


def xhtml2pdf_render_from_html(html, filename):
    """
    Convert a HTML text in PDF
    """
    response = HttpResponse(content_type='application/pdf')
    if filename:
        response['Content-Disposition'] = ('attachment; filename="%s"' %
                                           filename)
    pisa.CreatePDF(src=io.StringIO(html),
                   dest=response,
                   link_callback=xhtml2pdf_link_callback)
    return response


def xhtml2pdf_render_from_template_response(response, filename):
    """
    Convert a TemplateResponse object to PDF
    """
    return xhtml2pdf_render_from_html(
        html=response.render().content.decode('utf-8'),
        filename=filename)
