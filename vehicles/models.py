from django.db import models

# Create your models here.
class Vehicle(models.Model):
    VEHICLE_CHOICES = (("car", "car"), ("motorcycle", "motorcycle"))
    license_plate = models.CharField(max_length=255)
    vehicle_type = models.CharField(
        max_length=255, blank=False, null=False, choices=VEHICLE_CHOICES
    )
    arrived_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    amount_paid = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()
