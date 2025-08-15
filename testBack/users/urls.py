from django.urls import path
from .views import UserRegistrationView,TwoFactorVerificationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('verify-2fa/', TwoFactorVerificationView.as_view(), name='2fa-verify'),
    # ... інші URL для користувачів
]