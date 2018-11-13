from django.contrib import admin

from .models import (Continent,
                     Country,
                     Language)

# Register your models here.
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(Language)
