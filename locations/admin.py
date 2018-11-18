from django.contrib import admin

from .models import (Continent, ContinentAdmin,
                     Country, CountryAdmin,
                     Language, LanguageAdmin,
                     Location, LocationAdmin,
                     Position, PositionAdmin,
                     Region, RegionAdmin,
                     RegionAlias, RegionAliasAdmin)


# Register your models here.
admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(RegionAlias, RegionAliasAdmin)
