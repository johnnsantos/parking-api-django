from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, CredentialSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db import transaction


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=request.data["username"],
                    password=request.data["password"],
                    is_superuser=request.data["is_superuser"],
                    is_staff=request.data["is_staff"],
                )
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"error": "User already exists"}, status=status.HTTP_409_CONFLICT
            )


class LoginView(APIView):
    def post(self, request):
        serializer = CredentialSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({"token": token.key})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
