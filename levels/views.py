from rest_framework.generics import ListCreateAPIView
from .serializers import LevelSerializer
from .models import Level
from rest_framework.authentication import TokenAuthentication
from .permissions import AdminPostPermission


class ListCreateLevels(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPostPermission]

    queryset = Level.objects.all()
    serializer_class = LevelSerializer
