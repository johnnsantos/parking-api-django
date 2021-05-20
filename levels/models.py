from django.db import models

# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=255)
    fill_priority = models.IntegerField()
    motorcycle_spaces = models.IntegerField()
    car_spaces = models.IntegerField()
