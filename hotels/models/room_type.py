from django.db import models
from django.contrib import admin


class RoomType(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'hotels_roomtypes'
        ordering = ['name']

    def __str__(self):
        return self.name


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
