from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib import admin

from .views import EventAPIList, EventAPIDestroy, login_api_view, logout_api_view, csrf_view, AboutUserView, ClientViewSet

app_name = 'testter'  # Додаємо ім'я додатка

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')  # ✅ ViewSet підключається через router





urlpatterns = [

    path('events/', EventAPIList.as_view()), #+ post додає
    #path('events/<int:pk>/', EventAPIUpdate.as_view()),
    path('events/<int:pk>/', EventAPIDestroy.as_view()),
    path("login/", login_api_view),
    path("auth/logout", logout_api_view),
    path("auth/csrf/", csrf_view),
    path("auth/about_user", AboutUserView.as_view(), name='about_user'),
    path('', include(router.urls)),  # ✅ додаємо router.urls

]