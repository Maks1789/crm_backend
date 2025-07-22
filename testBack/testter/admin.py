from django.contrib import admin

# Register your models here.
from .models import Event, Client

admin.site.register(Event)

@admin.register(Client) # ✅ Реєструємо Client
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'fathers_name', 'email', 'phone_number', 'company', 'owner', 'is_active', 'last_contact')
    list_filter = ('is_active', 'owner', 'company')
    search_fields = ('full_name', 'email', 'phone_number', 'company', 'notes')
    raw_id_fields = ('owner',) # Зручно, якщо багато користувачів