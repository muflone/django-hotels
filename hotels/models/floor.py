from django.db import models

class Floor(models.Model):

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        # Define the database table
        db_table = 'floors'

    def __str__(self):
        return self.name
