from django.db import models

class Company(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    phone1 = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        # Define the database table
        db_table = 'companies'
