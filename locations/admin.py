from django.contrib import admin

from .models import (Continent,
                     Language)

# Register your models here.
admin.site.register(Continent)
admin.site.register(Language)
