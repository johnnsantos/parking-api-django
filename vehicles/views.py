from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from pricings.models import Pricing
from .serializers import VehicleSerializer
from .models import Vehicle
from levels.models import Level
from levels.serializers import LevelSerializer
from django.db.models import F
from datetime import datetime, timezone
import ipdb


class VehicleView(APIView):
    def put(self, request, vehicle_id):
        # pega o veiculo no banco
        vehicle = Vehicle.objects.get(id=vehicle_id)
        vehicle.paid_at = datetime.now(timezone.utc)

        # encontra o nivel onde o veiculo esta
        level = vehicle.level
        ipdb.set_trace()
        # calculando o pagamento
        # pega o ultimo preço registrado
        price = Pricing.objects.last()
        a = price.a_coefficient
        b = price.b_coefficient
        t = (vehicle.arrived_at - datetime.now(timezone.utc)).seconds / 3600
        payment = float("{:.2f}".format(a + b * t))

        vehicle.amount_paid = payment
        vehicle.space = None

        vehicle.save()

        serializer = VehicleSerializer(vehicle)

        response_data = {
            "license_plate": serializer.data["license_plate"],
            "vehicle_type": serializer.data["vehicle_type"],
            "arrived_at": serializer.data["arrived_at"],
            "paid_at": serializer.data["paid_at"],
            "amount_paid": serializer.data["amount_paid"],
            "space": None,
        }

        return Response(response_data)

    def post(self, request):

        # verifica se existe um preço, senao retorna 404
        price = Pricing.objects.last()
        if not price:
            return Response(
                {"error": "No created price yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # valida os dados de entrada da requisição
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
            return Response(
                {"error": "No empty entries or not created levels."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Tenta criar o veículo, se o tipo nao for car ou motorcycle ou se ja existir a placa no sistema, retorna erro
        try:
            vehicle = Vehicle.objects.create(**serializer.data)
        except:
            return Response(
                {"error": "incorrect params or vehicle already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        # tenta atualizar o nivel, se nao conseguir quer dizer que nao tem nivel criado e retorna 404
        try:
            Level.objects.filter(id=level.id).update(vehicles_set=vehicle)
        except:
            return Response(
                {"error": "Not created levels yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # se nao estourou nenhum dos erros acima podemos ocupar a vaga do nivel
        if request.data["vehicle_type"] == "car":
            Level.objects.filter(id=level.id).update(car_spaces=F("car_spaces") - 1)
        else:
            Level.objects.filter(id=level.id).update(
                motorcycle_spaces=F("motorcycle_spaces") - 1
            )

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
