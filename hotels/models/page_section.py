from django.db import models

class PageSection(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    header_title = models.CharField(max_length=255, blank=True)
    header_order = models.IntegerField()
    home_title = models.CharField(max_length=255, blank=True)
    home_order = models.IntegerField()
    home_image = models.CharField(max_length=255, blank=True)

    class Meta:
        # Define the database table
        db_table = 'page_sections'

    def __str__(self):
        return self.name

    def description_paragraphs(self):
        return self.description.replace('\r', '').split('\n\n')
