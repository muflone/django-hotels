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

import io
import os.path

from django.conf import settings
from django.http import HttpResponse

from xhtml2pdf import pisa


def xhtml2pdf_link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL    # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL     # Typically /static/media/
    mRoot = settings.MEDIA_ROOT   # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ''))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ''))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
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
