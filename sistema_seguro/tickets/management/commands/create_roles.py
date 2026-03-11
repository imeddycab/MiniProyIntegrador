from django.core.management.base import BaseCommand
from tickets.models import Rol

class Command(BaseCommand):
    help = 'Crear los roles iniciales del sistema'

    def handle(self, *args, **options):
        roles_data = [
            {'nombre': 'usuario', 'descripcion': 'Usuario del sistema con acceso básico'},
            {'nombre': 'admin', 'descripcion': 'Administrador del sistema con acceso total'},
            {'nombre': 'soporte', 'descripcion': 'Personal de soporte técnico'},
        ]
        
        for role_info in roles_data:
            rol, created = Rol.objects.get_or_create(
                nombre=role_info['nombre'],
                defaults={'descripcion': role_info['descripcion']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Rol "{rol.nombre}" creado exitosamente')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ El rol "{rol.nombre}" ya existe')
                )
        
        self.stdout.write(self.style.SUCCESS('\n✓ Roles inicializados correctamente'))
