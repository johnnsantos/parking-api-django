from django.db import models

# Create your models here.
class Pricing(models.Model):
    a_coefficient = models.IntegerField()
    b_coefficient = models.IntegerField()
