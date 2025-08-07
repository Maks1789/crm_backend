
from rest_framework import viewsets, permissions, generics  # Додано імпорт permissions
from .models import Event, Client

from .serializers import EventSerializer, ClientSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .permission import IsOwner
@ensure_csrf_cookie
def csrf_view(request):
    return JsonResponse({"detail": "CSRF cookie set"})



@require_POST
#@csrf_exempt
def login_api_view(request):
    from django.http import QueryDict
    data = request.POST or QueryDict(request.body)
    print(dict(request.headers))
    username = data.get("username")
    password = data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"username": user.username})
    return JsonResponse({"detail": "Invalid credentials"}, status=401)


@require_POST
#@csrf_exempt  # (або залишити з CSRF, якщо frontend додає X-CSRFToken)
def logout_api_view(request):
    logout(request)  # ← це знищує сесію в Django
    return JsonResponse({"detail": "Logged out"}, status=200)

class EventAPIList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)



class AboutUserView(APIView):
    # ✅ Це забезпечує, що View доступний лише автентифікованим користувачам.
    # Якщо користувач не автентифікований, DRF автоматично поверне 401 Unauthorized
    # з JSON-повідомленням про помилку ("Authentication credentials were not provided.").
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # request.user буде об'єктом User (якщо користувач автентифікований)
        user_data = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_superuser': request.user.is_superuser,
            'is_staff': request.user.is_staff,
        }
        # ✅ Використовуємо DRF Response, який встановлює Content-Type: application/json
        return Response(user_data, status=status.HTTP_200_OK)


# --- НОВИЙ CLIENT VIEWSET ---
class ClientViewSet(viewsets.ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated] # Захищаємо доступ

    def get_queryset(self):
        # ✅ Користувач бачить лише своїх клієнтів
        return Client.objects.filter(owner=self.request.user).order_by('last_name')

    def perform_create(self, serializer):
        # ✅ Автоматично встановлює власника на поточного користувача
        serializer.save(owner=self.request.user)


"""@login_required  # ✅ Перевірка, що користувач авторизований
def about_user(request):
    user = request.user  # 🔑 Отримуємо авторизованого користувача
    print(f"USER = = = {user}")

    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,

    }, status=200)
"""


# class EventAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated]


