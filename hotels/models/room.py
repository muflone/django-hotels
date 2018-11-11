from django.db import models

class Room(models.Model):

    building = models.ForeignKey('Building',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    room_type = models.ForeignKey('RoomType',
                                  on_delete=models.CASCADE)
    floor = models.ForeignKey('Floor',
                              on_delete=models.CASCADE)

    class Meta:
        # Define the database table
        db_table = 'rooms'

    def __str__(self):
        return self.name
