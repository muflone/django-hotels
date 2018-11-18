from django.db import models
from django.contrib import admin


class Building(models.Model):

    hotel = models.ForeignKey('Hotel',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    floors = models.IntegerField(blank=False)

    address = models.TextField(blank=True)
    phone1 = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    class Meta:
        # Define the database table
        db_table = 'hotels_buildings'

    def __str__(self):
        return self.name


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'floors')
    list_filter = ('hotel', )
