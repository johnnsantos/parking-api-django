from django.db import models
from vehicles.models import Vehicle

# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=255)
    fill_priority = models.IntegerField()
    motorcycle_spaces = models.IntegerField()
    car_spaces = models.IntegerField()
    vehicles_set = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        related_name="level",
    )
