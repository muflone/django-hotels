from django.db import models
from django.contrib import admin

from .country import Country
from .position import Position
from .region_alias import RegionAlias


class Region(models.Model):

    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE)
    aliases = models.ManyToManyField(RegionAlias,
                                     db_table='locations_region_aliases')

    class Meta:
        # Define the database table
        db_table = 'locations_regions'
        ordering = ['name']
        unique_together = ('name', 'country')

    def __str__(self):
        return '{COUNTRY} - {NAME}'.format(COUNTRY=self.country.name,
                                           NAME=self.name)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'country', 'position')
    list_filter = ('country', 'position')
