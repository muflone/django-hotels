from django.db import models
from django.contrib import admin


class Continent(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'locations_continents'
        ordering = ['name']

    def __str__(self):
        return self.name


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
