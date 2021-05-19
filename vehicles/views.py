from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from pricings.models import Pricing
from django.http import Http404
from .serializers import VehicleSerializer
from .models import Vehicle
from levels.models import Level
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
                Level.objects.order_by("fill_priority")
                .filter(car_spaces__gte=1)
                .first()
            )
        else:
            level = (
                Level.objects.order_by("fill_priority")
                .filter(motorcycle_spaces__gte=1)
                .first()
            )

        if level == []:
            raise Http404("No empty entries or not created levels.")

        # cria o veículo
        vehicle = Vehicle.objects.create(**serializer.data)
        ipdb.set_trace()

        level.vehicles_set.add(vehicle)

        serializer = VehicleSerializer(vehicle)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
