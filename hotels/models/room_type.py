from django.db import models

class RoomType(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        # Define the database table
        db_table = 'hotels_roomtypes'

    def __str__(self):
        return self.name