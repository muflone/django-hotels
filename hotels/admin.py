from django.contrib import admin

from .models import Company, Hotel, Floor, Building, RoomType, Room

# Register your models here.
admin.site.register(Company)
admin.site.register(Hotel)
admin.site.register(Floor)
admin.site.register(Building)
admin.site.register(RoomType)
admin.site.register(Room)
