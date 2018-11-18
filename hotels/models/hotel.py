from django.db import models
from django.contrib import admin


class Hotel(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone1 = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    company = models.ForeignKey('Company',
                                on_delete=models.CASCADE)

    class Meta:
        # Define the database table
        db_table = 'hotels_hotels'

    def __str__(self):
        return self.name


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'description')
