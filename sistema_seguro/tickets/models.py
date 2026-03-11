from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    class Meta:
        ordering = ['-fecha_creacion']  # Tickets más recientes primero
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"