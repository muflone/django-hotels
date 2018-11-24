from django.db import models
from django.contrib import admin


class Brand(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'hotels_brands'
        ordering = ['name']

    def __str__(self):
        return self.name


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
