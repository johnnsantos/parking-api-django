from rest_framework import serializers
from .models import Level


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"

    def to_representation(self, instance):
        data = {
            "id": instance.id,
            "name": instance.name,
            "fill_priority": instance.fill_priority,
            "available_spaces": {
                "available_motorcycle_spaces": instance.motorcycle_spaces,
                "available_car_spaces": instance.car_spaces,
            },
        }
        return data
