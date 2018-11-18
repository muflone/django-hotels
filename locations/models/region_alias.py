from django.db import models
from django.contrib import admin

from .country import Country


class RegionAlias(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)

    class Meta:
        # Define the database table
        db_table = 'locations_regions_aliases'
        ordering = ['name']
        verbose_name_plural = 'Region Aliases'
        unique_together = ('name', 'country')

    def __str__(self):
        return '{COUNTRY} - {NAME}'.format(COUNTRY=self.country.name,
                                           NAME=self.name)


class RegionAliasAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'country')
    list_filter = ('country', )
