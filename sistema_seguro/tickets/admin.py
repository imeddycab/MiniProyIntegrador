from django.contrib import admin
from .models import Ticket, Rol, UserProfile

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'estado', 'creado_en']
    list_filter = ['estado', 'creado_en']
    search_fields = ['titulo', 'descripcion']
