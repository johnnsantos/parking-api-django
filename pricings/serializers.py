from rest_framework import serializers
from .models import Pricing


class PrincingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = "__all__"
