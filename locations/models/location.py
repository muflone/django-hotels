from django.db import models
from django.contrib import admin

from .country import Country
from .region import Region


class Location(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'locations_locations'
        ordering = ['name']

    def __str__(self):
        return self.name


class LocationAdminCountryFilter(admin.SimpleListFilter):
    title = 'country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        return Country.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region__country=self.value())


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'country')
    list_filter = (LocationAdminCountryFilter, 'region')

    def country(self, instance):
        return instance.region.country
    country.short_description = 'Country'
