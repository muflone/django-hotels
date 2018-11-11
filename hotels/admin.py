from django.contrib import admin

from .models import Company, Hotel, Floor, Building

# Register your models here.
admin.site.register(Company)
admin.site.register(Hotel)
admin.site.register(Floor)
admin.site.register(Building)
