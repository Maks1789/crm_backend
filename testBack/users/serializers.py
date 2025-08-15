# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile
import pyotp


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'telegram_id', 'address', 'company', 'created_at', 'last_login', 'failed_otp_attempts', 'otp_lockout_until']


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile', 'qr_code']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'qr_code': {'read_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        secret = pyotp.random_base32()

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False  # Користувач неактивний до підтвердження 2FA
        )

        UserProfile.objects.create(user=user, totp_secret=secret, **profile_data)

        return user

    def get_qr_code(self, obj):
        if hasattr(obj, 'profile'):
            otp_auth_url = pyotp.totp.TOTP(obj.profile.totp_secret).provisioning_uri(
                name=obj.username,
                issuer_name='Your сrm'
            )
            return otp_auth_url
        return None


class TwoFactorVerificationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data.get('username')
        otp_code = data.get('otp_code')

        try:
            user = User.objects.get(username=username)
            profile = user.profile
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            raise serializers.ValidationError("Недійсний користувач.")

        # Перевірка на тимчасове блокування
        if profile.otp_lockout_until and timezone.now() < profile.otp_lockout_until:
            remaining_time = profile.otp_lockout_until - timezone.now()
            raise serializers.ValidationError(f"Забагато невдалих спроб. Спробуйте ще раз через {int(remaining_time.total_seconds())} секунд.")

        if user.is_active:
            raise serializers.ValidationError("Акаунт уже активовано.")

        totp = pyotp.TOTP(profile.totp_secret)
        if totp.verify(otp_code):
            # Успішна перевірка: скидаємо лічильник
            profile.failed_otp_attempts = 0
            profile.otp_lockout_until = None
            profile.save()
        else:
            # Невдала спроба: збільшуємо лічильник
            profile.failed_otp_attempts += 1
            if profile.failed_otp_attempts >= 5: # Максимум 5 спроб
                profile.otp_lockout_until = timezone.now() + timedelta(minutes=15) # Блокування на 15 хвилин
                profile.failed_otp_attempts = 0
            profile.save()
            raise serializers.ValidationError("Невірний код TOTP.")

        return data







'''
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
import pyotp


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'telegram_id', 'address', 'company', 'created_at', 'last_login']


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile', 'qr_code']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'qr_code': {'read_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        secret = pyotp.random_base32()

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_active=False  # Користувач неактивний до підтвердження 2FA
        )

        UserProfile.objects.create(user=user, totp_secret=secret, **profile_data)

        return user

    def get_qr_code(self, obj):
        if hasattr(obj, 'profile'):
            otp_auth_url = pyotp.totp.TOTP(obj.profile.totp_secret).provisioning_uri(
                name=obj.username,
                issuer_name='Your сrm'
            )
            return otp_auth_url
        return None


class TwoFactorVerificationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data.get('username')
        otp_code = data.get('otp_code')

        try:
            user = User.objects.get(username=username)
            profile = user.profile
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            raise serializers.ValidationError("Недійсний користувач.")

        if user.is_active:
            raise serializers.ValidationError("Акаунт уже активовано.")

        totp = pyotp.TOTP(profile.totp_secret)
        if not totp.verify(otp_code):
            raise serializers.ValidationError("Невірний код TOTP.")

        return data


'''