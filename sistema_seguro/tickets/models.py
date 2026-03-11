from django.db import models
from django.contrib.auth.models import User

class Rol(models.Model):
    ROLES = (
        ('usuario', 'Usuario Normal'),
        ('admin', 'Administrador'),
        ('soporte', 'Soporte'),
    )
    nombre = models.CharField(max_length=20, choices=ROLES, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.get_nombre_display()

class UserProfile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"

class Ticket(models.Model):
    ESTADOS = (
        ('abierto', 'Abierto'),
        ('en_progreso', 'En Progreso'),
        ('cerrado', 'Cerrado'),
    )
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='abierto')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-creado_en']