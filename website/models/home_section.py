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

from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class HomeSection(BaseModel):
    name = models.CharField(max_length=255,
                            primary_key=True,
                            verbose_name=pgettext_lazy('HomeSection',
                                                       'name'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('HomeSection',
                                                              'description'))
    link = models.CharField(max_length=255,
                            blank=True,
                            verbose_name=pgettext_lazy('HomeSection',
                                                       'link'))
    header_title = models.CharField(max_length=255,
                                    blank=True,
                                    verbose_name=pgettext_lazy('HomeSection',
                                                               'header title'))
    header_order = models.IntegerField(verbose_name=pgettext_lazy(
        'HomeSection',
        'header order'))
    home_title = models.CharField(max_length=255,
                                  blank=True,
                                  verbose_name=pgettext_lazy('HomeSection',
                                                             'home title'))
    home_order = models.IntegerField(verbose_name=pgettext_lazy('HomeSection',
                                                                'home order'))
    home_image = models.CharField(max_length=255,
                                  blank=True,
                                  verbose_name=pgettext_lazy('HomeSection',
                                                             'home image'))
    login_required = models.BooleanField(default=False,
                                         verbose_name=pgettext_lazy(
                                             'HomeSection',
                                             'login required'))
    admin_login_required = models.BooleanField(default=False,
                                               verbose_name=pgettext_lazy(
                                                   'HomeSection',
                                                   'admin login required'))

    class Meta:
        # Define the database table
        db_table = 'website_home_sections'
        ordering = ['header_order']
        verbose_name = pgettext_lazy('HomeSection',
                                     'Home Section')
        verbose_name_plural = pgettext_lazy('HomeSection',
                                            'Home Sections')

    def __str__(self):
        return self.name


class HomeSectionAdmin(BaseModelAdmin):
    pass
