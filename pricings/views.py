from rest_framework.generics import CreateAPIView
from .serializers import PrincingSerializer
from .models import Pricing
from levels.permissions import AdminPostPermission
from rest_framework.authentication import TokenAuthentication


class ListCreatePricing(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPostPermission]

    queryset = Pricing.objects.all()
    serializer_class = PrincingSerializer
