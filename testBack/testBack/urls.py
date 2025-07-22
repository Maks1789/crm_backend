from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    #session
    path('auth/', include('rest_framework.urls')),
    path('', include('testter.urls', namespace='testter'))

    ]