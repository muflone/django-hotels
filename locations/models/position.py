from django.db import models

class Position(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'locations_positions'

    def __str__(self):
        return self.name
