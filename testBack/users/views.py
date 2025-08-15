# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, authenticate
from .serializers import (
    UserRegistrationSerializer,
    TwoFactorVerificationSerializer
)
from .models import UserProfile, User


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "Акаунт створено. Відскануйте QR-код для завершення реєстрації.",
            "qr_code": serializer.data['qr_code'],
            "username": serializer.data['username']
        }, status=status.HTTP_201_CREATED)


class TwoFactorVerificationView(generics.GenericAPIView):
    serializer_class = TwoFactorVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        user = User.objects.get(username=username)

        user.is_active = True
        user.save()

        user.profile.is_2fa_enabled = True
        user.profile.totp_secret = None
        user.profile.save()

        login(request, user)

        return Response({"message": "Акаунт успішно активовано."}, status=status.HTTP_200_OK)


