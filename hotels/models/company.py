from django.db import models
from django.contrib import admin


class Company(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone1 = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    vat_number = models.CharField(max_length=255, blank=True)
    tax_code = models.CharField(max_length=255, blank=True)

    class Meta:
        # Define the database table
        db_table = 'hotels_companies'
        ordering = ['name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
