from django.db import models
from django.contrib import admin

from .company import Company


class Building(models.Model):

    hotel = models.ForeignKey('Hotel',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    floors = models.PositiveIntegerField(blank=False)
    address = models.TextField(blank=True)
    location = models.ForeignKey('locations.Location',
                                 on_delete=models.CASCADE,
                                 default=0)
    postal_code = models.CharField(max_length=15, blank=True)
    phone1 = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    class Meta:
        # Define the database table
        db_table = 'hotels_buildings'

    def __str__(self):
        return self.name


class BuildingAdminCompanyFilter(admin.SimpleListFilter):
    title = 'company'
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        return Company.objects.all().values_list('name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(hotel__company=self.value())


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'floors', 'company')
    list_filter = (BuildingAdminCompanyFilter, 'hotel')

    def company(self, instance):
        return instance.hotel.company
    company.short_description = 'Company'
