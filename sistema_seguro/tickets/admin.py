from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'usuario', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('usuario', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    list_per_page = 20
    
    fieldsets = (
        ('Información del Ticket', {
            'fields': ('titulo', 'descripcion', 'usuario')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )