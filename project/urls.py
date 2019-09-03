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

"""Django Hotels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


# Define routes
urlpatterns = []
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # Import Django Debug Toolbar
    try:
        # noinspection PyPackageRequirements
        import debug_toolbar
        urlpatterns.append(path('__debug__', include(debug_toolbar.urls)))
    except ImportError:
        # Django Debug Toolbar package unavailable
        pass

# Add i18n prefixes for sections
urlpatterns += i18n_patterns(
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.WORK_URL, include('work.urls')),
    prefix_default_language=True
)

# Add standard paths
urlpatterns.append(path(settings.EXPLORER_URL, include('explorer.urls')))
urlpatterns.append(path(settings.ADMIN_URL, admin.site.urls))
urlpatterns.append(path(settings.WORK_URL, include('work.urls')))
urlpatterns.append(path(settings.API_URL, include('jsonapi.urls')))
# Enable iprestrict URL if application is enabled
if 'iprestrict' in settings.INSTALLED_APPS:
    urlpatterns.append(path(settings.IPRESTRICT_URL,
                       include('iprestrict.urls', namespace='iprestrict')))
# Include catch-all page
urlpatterns.append(path('', include('website.urls')))
