from django.db import models
from django.contrib import admin

from .hotel import Hotel


class Room(models.Model):

    building = models.ForeignKey('Building',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    room_type = models.ForeignKey('RoomType',
                                  on_delete=models.CASCADE)
    bed_type = models.ForeignKey('BedType',
                                  on_delete=models.CASCADE,
                                  default='UNKNOWN')
    phone1 = models.CharField(max_length=255, blank=True)
    seats_base = models.PositiveIntegerField(default=1)
    seats_additional = models.PositiveIntegerField(default=0)

    class Meta:
        # Define the database table
        db_table = 'hotels_rooms'
        ordering = ['building', 'name']
        unique_together = ('building', 'name')

    def __str__(self):
        return '{BUILDING} - {NAME}'.format(BUILDING=self.building.name,
                                            NAME=self.name)


class RoomAdminHotelFilter(admin.SimpleListFilter):
    title = 'hotel'
    parameter_name = 'hotel'

    def lookups(self, request, model_admin):
        return Hotel.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(building__hotel=self.value())


class RoomAdmin(admin.ModelAdmin):
    list_display = ('building', 'name', 'room_type')
    list_filter = (RoomAdminHotelFilter, 'building', 'room_type')
