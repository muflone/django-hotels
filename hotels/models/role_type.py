from django.db import models


class RoleType(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'hotels_roletypes'
        ordering = ['name']

    def __str__(self):
        return self.name
