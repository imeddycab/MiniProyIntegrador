from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tickets.models import Rol, UserProfile

class Command(BaseCommand):
    help = 'Crear un usuario administrador'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')
        parser.add_argument('password', type=str, help='Contraseña')
        parser.add_argument('--email', type=str, default='admin@sistema.com', help='Email del usuario')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'✗ El usuario "{username}" ya existe')
            )
            return

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=False
        )

        # Obtener el rol de admin
        try:
            rol_admin = Rol.objects.get(nombre='admin')
            UserProfile.objects.create(usuario=user, rol=rol_admin)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario administrador "{username}" creado exitosamente')
            )
        except Rol.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('✗ El rol "admin" no existe. Ejecuta "create_roles" primero')
            )
