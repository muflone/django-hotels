from django.contrib import admin

from .models import (Continent, ContinentAdmin,
                     Country, CountryAdmin,
                     Language, LanguageAdmin,
                     Position, PositionAdmin,
                     Region, RegionAdmin)


# Register your models here.
admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Region, RegionAdmin)
