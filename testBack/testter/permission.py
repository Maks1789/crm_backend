from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        #return request.user and (request.user.is_staff or obj.owner == request.user)
        user = request.user
        print("🔍 Користувач:", user)
        print("🔐 is_authenticated:", user.is_authenticated)
        print("🔐 is_staff:", user.is_staff)
        print("📦 Об'єкт:", obj)
        print("👤 Власник об'єкта:", getattr(obj, 'owner', None))

        result = user.is_staff or (hasattr(obj, 'owner') and obj.owner == user)
        print("✅ Доступ дозволено?" , result)

        return result

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

import logging
from rest_framework.permissions import SAFE_METHODS, BasePermission

logger = logging.getLogger(__name__)

class VerboseAdminOrReadOnly(BasePermission):
    """
    Дозволяє тільки адміністраторам змінювати дані.
    Всім іншим дозволено тільки читання.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        if not user or not user.is_authenticated:
            logger.warning(f"❌ Access denied: неавтентифікований користувач при {request.method} на {request.path}")
            return False

        if not user.is_staff:
            logger.warning(f"❌ Access denied: користувач {user.username} не є адміном")
            return False

        return True


