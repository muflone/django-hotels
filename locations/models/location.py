from django.db import models
from django.contrib import admin

from .country import Country
from .region import Region


class Location(models.Model):

    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    province = models.CharField(max_length=255,
                                blank=True,
                                null=True)

    class Meta:
        # Define the database table
        db_table = 'locations_locations'
        ordering = ['name']
        unique_together = ('province', 'name')

    def __str__(self):
        return '{NAME} ({PROVINCE})'.format(NAME=self.name,
                                            PROVINCE=self.province)


class LocationAdminInputFilter(admin.SimpleListFilter):
    template = 'locations/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return (('', ''),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class LocationAdminCountryFilter(admin.SimpleListFilter):
    title = 'country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        return Country.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region__country=self.value())


class LocationAdminNameFilter(LocationAdminInputFilter):
    parameter_name = 'name'
    title = 'name'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name=self.value())


class LocationAdminProvinceFilter(LocationAdminInputFilter):
    parameter_name = 'province'
    title = 'province'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(province=self.value())


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'region', 'country')
    list_filter = (LocationAdminNameFilter,
                   LocationAdminProvinceFilter,
                   LocationAdminCountryFilter,
                   'region')

    def country(self, instance):
        return instance.region.country
    country.short_description = 'Country'
