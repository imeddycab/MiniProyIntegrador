# 🔐 Sistema Seguro - Guía de Uso

## Información General
Este es un sistema seguro de gestión de tickets con roles y permisos. El proyecto incluye:
- ✅ Autenticación y autorización
- ✅ Panel de administrador protegido
- ✅ Gestión de roles (Usuario, Admin, Soporte)
- ✅ Gestión de tickets con estados

## Credenciales de Prueba

**Usuario Administrador:**
- **Usuario:** `admin`
- **Contraseña:** `admin123`

## Flujo de la Aplicación

### 1. Registro (Nuevo Usuario)
```
http://127.0.0.1:8000/registro/
```
- Crea una nueva cuenta
- Acceso automático como usuario normal
- Después de registrarse, puedes iniciar sesión

### 2. Login (Iniciar Sesión)
```
http://127.0.0.1:8000/login/
```
- Ingresa con tus credenciales
- Se redirige automáticamente al dashboard

### 3. Dashboard (Pantalla Protegida)
```
http://127.0.0.1:8000/
```
- Bienvenida después de iniciar sesión
- Visualiza tus tickets asignados
- Acceso a mis tickets y panel de admin (si eres admin)

### 4. Mis Tickets
```
http://127.0.0.1:8000/lista/
```
- **Usuario Normal:** Ve solo sus tickets
- **Administrador:** Ve todos los tickets del sistema

### 5. Panel de Administrador (Protegido)
```
http://127.0.0.1:8000/admin-panel/
```
- **Solo para administradores**
- Dashboard con estadísticas:
  - Total de usuarios
  - Total de tickets
  - Tickets abiertos/cerrados
- Listado de usuarios activos
- Últimos tickets registrados

## Estructura de Roles

### Usuario Normal
- Ver solo sus propios tickets
- Crear y gestionar sus tickets

### Administrador (Admin)
- Ver todos los tickets
- Acceso al panel de administración
- Ver estadísticas del sistema
- Ver lista completa de usuarios

### Soporte
- Rol disponible para futuras extensiones

## Modelos de Base de Datos

### Usuario (User)
- username, email, password
- is_active, is_staff, date_joined

### UserProfile
- Relación 1:1 con User
- Asignación de Rol

### Rol
- Tipos: usuario, admin, soporte
- Descripción de cada rol

### Ticket
- titulo, descripcion
- usuario (FK)
- estado (abierto, en_progreso, cerrado)
- creado_en, actualizado_en

## Configuración de Seguridad

El proyecto incluye:
```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 1800  # 30 minutos
```

## URLs Disponibles

| URL | Nombre | Descripción |
|-----|--------|-------------|
| `/admin/` | admin | Panel de administración de Django |
| `/login/` | login | Iniciar sesión |
| `/logout/` | logout | Cerrar sesión |
| `/` | dashboard | Pantalla principal (protegida) |
| `/registro/` | registro | Crear nueva cuenta |
| `/lista/` | lista | Listado de tickets |
| `/admin-panel/` | admin_panel | Panel de administrador (protegido) |

## Decoradores Personalizados

### @admin_required
Protege vistas solo para administradores
```python
@admin_required
def admin_panel(request):
    # Solo acceden administradores
```

### @login_required
Protege vistas solo para usuarios autenticados
```python
@login_required
def dashboard(request):
    # Solo usuarios logueados
```

## Comandos Útiles

### Crear roles iniciales
```bash
python manage.py create_roles
```

### Crear usuario administrador
```bash
python manage.py create_admin <username> <password>
```

### Hacer migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Iniciar servidor
```bash
python manage.py runserver
```

## Próximas Mejoras

- [ ] Crear tickets desde el dashboard
- [ ] Editar/eliminar tickets
- [ ] Asignar tickets a usuarios
- [ ] Sistema de comentarios en tickets
- [ ] Notificaciones por email
- [ ] Exportar reportes
- [ ] 2FA (Two-Factor Authentication)

---
**Sistema Corporativo Seguro © 2026**
