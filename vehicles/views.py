from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from pricings.models import Pricing
from django.http import Http404
from .serializers import VehicleSerializer
from .models import Vehicle
from levels.models import Level
from levels.serializers import LevelSerializer
import ipdb


class VehicleView(APIView):
    def post(self, request):

        # verifica se existe um preço, senao retorna 404
        try:
            Pricing.objects.last()
        except:
            raise Http404("No price created yet.")

        serializer = VehicleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # encontra o nivel de acordo com prioridade e numero de vagas, se nao tiver niveis ou nao tiver vagas retorna 404
        if request.data["vehicle_type"] == "car":
            level = (
                Level.objects.order_by("-fill_priority")
                .filter(car_spaces__gte=1)
                .first()
            )
        else:
            level = (
                Level.objects.order_by("-fill_priority")
                .filter(motorcycle_spaces__gte=1)
                .first()
            )

        if level == []:
            raise Http404("No empty entries or not created levels.")

        # cria o veículo
        try:
            vehicle = Vehicle.objects.create(**serializer.data)
        except:
            return Response(
                {"error": "incorrect params or vehicle already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        Level.objects.filter(id=level.id).update(vehicles_set=vehicle)

        serializer = VehicleSerializer(vehicle)
        level_serializer = LevelSerializer(level)

        response_data = {
            "id": serializer.data["id"],
            "license_plate": serializer.data["license_plate"],
            "vehicle_type": serializer.data["vehicle_type"],
            "arrived_at": serializer.data["arrived_at"],
            "paid_at": serializer.data["paid_at"],
            "amount_paid": serializer.data["amount_paid"],
            "space": {
                "id": level_serializer.data["id"],
                "variety": serializer.data["vehicle_type"],
                "level_name": level_serializer.data["name"],
            },
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
