from django.db import models
from django.contrib import admin

from .continent import Continent
from .language import Language


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
