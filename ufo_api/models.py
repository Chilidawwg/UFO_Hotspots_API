from django.db import models

# Create your models here.


date_time = 'id'


class Sighting(models.Model):
    date_time = models.CharField(primary_key=True, max_length=100)
    shape = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    comments = models.TextField(max_length=100)

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return self.date_time