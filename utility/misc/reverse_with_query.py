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

from django.urls import reverse
from django.utils.http import urlencode


def reverse_with_query(view, args=None, kwargs=None, query=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = reverse_with_query(view='my_test_url',
                             args=[2, ],
                             kwargs={'pk': object.id},
                             query_kwargs={'next': reverse('home')})
    """
    url = reverse(view, args=args, kwargs=kwargs)
    if query:
        return '{URL}?{QUERY}'.format(URL=url, QUERY=urlencode(query))
    else:
      return url
