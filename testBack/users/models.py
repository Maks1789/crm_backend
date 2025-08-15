# models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    telegram_id = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True)
    company = models.CharField(max_length=60, blank=True)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    language = models.CharField(max_length=5, default='uk')
    timezone = models.CharField(max_length=50, default='Europe/Kiev')

    # Поля для 2FA
    is_2fa_enabled = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=64, blank=True, null=True)

    is_subscribed_to_newsletter = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Нові поля для Rate Limiting
    failed_otp_attempts = models.IntegerField(default=0)
    otp_lockout_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'