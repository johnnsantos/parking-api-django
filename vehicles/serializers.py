from rest_framework import serializers
from .models import Vehicle
from levels.serializers import LevelSerializer


class VehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    license_plate = serializers.CharField()
    vehicle_type = serializers.CharField()
    arrived_at = serializers.DateTimeField(read_only=True)
    paid_at = serializers.DateTimeField(read_only=True)
    amount_paid = serializers.FloatField(read_only=True)
