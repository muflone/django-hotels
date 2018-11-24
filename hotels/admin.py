from django.contrib import admin

from .models import (BedType, BedTypeAdmin,
                     Brand, BrandAdmin,
                     Company, CompanyAdmin,
                     Hotel, HotelAdmin,
                     Building, BuildingAdmin,
                     RoomType, RoomTypeAdmin,
                     Room, RoomAdmin,
                     RoleType,
                     PageSection)

# Register your models here.
admin.site.register(BedType, BedTypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoleType)
admin.site.register(PageSection)
