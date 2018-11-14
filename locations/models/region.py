from django.db import models

from .country import Country
from .position import Position

class Region(models.Model):

    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE)

    class Meta:
        # Define the database table
        db_table = 'locations_regions'
        ordering = ['name']
        unique_together = ('name', 'country')

    def __str__(self):
        return '{COUNTRY} - {NAME}'.format(COUNTRY=self.country.name,
                                           NAME=self.name)
