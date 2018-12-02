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

import csv
import io

from django.db import models
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path

from .continent import Continent
from .language import Language

from ..forms import CSVImportForm


class Country(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)
    capital = models.CharField(max_length=255, blank=True)
    continent = models.ForeignKey(Continent,
                                  on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language)

    class Meta:
        # Define the database table
        db_table = 'locations_countries'
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'continent')
    list_filter = ('continent', )
    change_list_template = 'utility/import_csv/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        def append_error(type_name, item):
            """Append an error message to the messages list"""
            error_message = 'Unexpected {TYPE} "{ITEM}"'.format(TYPE=type_name,
                                                                ITEM=item)
            if error_message not in error_messages:
                error_messages.append(error_message)
                self.message_user(request, error_message, messages.ERROR)

        if request.method == "POST":
            # Preload continents
            continents = {}
            for item in Continent.objects.all():
                continents[item.name] = item
            # Preload languages
            languages = {}
            for item in Language.objects.all():
                languages[item.name] = item
            # Load CSV file content
            csv_file = io.TextIOWrapper(
                request.FILES['csv_file'].file,
                encoding=request.POST['encoding'])
            reader = csv.DictReader(
                csv_file,
                delimiter=request.POST['delimiter'])
            # Load data from CSV
            error_messages = []
            countries = []
            country_language = {}
            for row in reader:
                if row['CONTINENT'] not in continents:
                    append_error('continent', row['CONTINENT'])
                elif row['LANGUAGE'] not in languages:
                    append_error('language', row['LANGUAGE'])
                else:
                    # If no error create a new Country object
                    country = Country(name=row['NAME'],
                                      description=row['DESCRIPTION'],
                                      capital=row['CAPITAL'],
                                      continent=continents[row['CONTINENT']])
                    country_language[row['NAME']] = row['LANGUAGE']
                    countries.append(country)
            # Save data only if there were not errors
            if not error_messages:
                Country.objects.bulk_create(countries)
                self.message_user(request, 'Your CSV file has been imported')
                # Add language in each country
                for country in countries:
                    country.languages.set(
                        (languages[country_language[country.name]], ))
            return redirect('..')
        return render(request,
                      'locations/form_csv_import.html',
                      {'form': CSVImportForm()})
