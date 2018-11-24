from django.db import models
from django.contrib import admin


class Floor(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        # Define the database table
        db_table = 'hotels_floors'
        ordering = ['name']

    def __str__(self):
        return self.name


class FloorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
