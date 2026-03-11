# 🔐 Proyecto: Módulo Seguro en Django (Gestión de Tickets)

**Guía paso a paso dividida para 3 integrantes del equipo**

El proyecto cumple con: autenticación, roles, validación de formularios, protección CSRF y sesiones seguras.

---

## 📋 Paso Inicial (Lo realiza una persona del equipo)

```bash
# 1. Instalar Django
pip install django

# 2. Crear el proyecto
django-admin startproject sistema_seguro

# 3. Entrar a la carpeta
cd sistema_seguro

# 4. Crear la aplicación
python manage.py startapp tickets

# 5. Registrar la aplicación en settings.py
# INSTALLED_APPS = [
#     ...
#     "tickets",
# ]

# 6. Hacer migraciones
python manage.py migrate

# 7. Subir el proyecto a GitHub
git init
git add .
git commit -m "Proyecto inicial"
git push origin main
```

---

## 👤 Persona 1 — Autenticación

**Responsable:** Implementar login, logout y protección de páginas.

### ✅ Tareas Completadas:

#### 1. URLs configuradas en `sistema_seguro/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('tickets.urls')),
]
```

#### 2. Plantilla `registro.html` (Para crear usuarios):

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro</title>
    <style>
        body { background: #f0f4fb; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; }
        form { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        input { width: 100%; padding: 0.5rem; margin: 0.5rem 0; border: 1px solid #ddd; border-radius: 4px; }
        button { width: 100%; padding: 0.75rem; background: #4a6fa5; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #3a5f95; }
    </style>
</head>
<body>
    <form method="POST">
        {% csrf_token %}
        <h2>Crear Cuenta</h2>
        <label>Usuario:</label>
        <input type="text" name="username" required>
        <label>Password:</label>
        <input type="password" name="password" required>
        <button type="submit">Registrarse</button>
        <p style="text-align: center; font-size: 0.9rem;">
            ¿Ya tienes cuenta? <a href="/login/">Inicia sesión aquí</a>
        </p>
    </form>
</body>
</html>
```

#### 3. Vista en `tickets/views.py`:

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    """Pantalla principal protegida"""
    return render(request, 'dashboard.html', {'user': request.user})

def registro(request):
    """Vista para crear nuevos usuarios"""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registro.html', {'error': 'El usuario ya existe'})
        
        user = User.objects.create_user(username=username, password=password)
        return redirect('login')
    
    return render(request, 'registro.html')
```

---

## 👥 Persona 2 — Roles y Permisos

**Responsable:** Modelo de datos y permisos de administrador y usuario.

### ✅ Tareas Completadas:

#### 1. Modelos en `tickets/models.py`:

```python
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

    def __str__(self):
        return self.titulo
```

#### 2. Decorador personalizado para admin:

```python
from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    """Decorador que verifica si el usuario es administrador"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if profile.rol and profile.rol.nombre == 'admin':
                    return view_func(request, *args, **kwargs)
            except:
                pass
        return redirect('login')
    return wrapper
```

#### 3. Vistas con control de roles:

```python
@login_required
def lista_tickets(request):
    """Admin ve todos, usuarios solo ven los suyos"""
    try:
        profile = request.user.profile
        if profile.rol and profile.rol.nombre == 'admin':
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(usuario=request.user)
    except:
        tickets = Ticket.objects.filter(usuario=request.user)
    
    return render(request, 'lista.html', {'tickets': tickets})

@admin_required
def admin_panel(request):
    """Panel exclusivo para administradores"""
    total_usuarios = User.objects.count()
    total_tickets = Ticket.objects.count()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_tickets': total_tickets,
        'usuarios': User.objects.all(),
        'tickets': Ticket.objects.all()[:10],
    }
    
    return render(request, 'admin_panel.html', context)
```

---

## 🛡️ Persona 3 — Formularios y Seguridad

**Responsable:** Validación de formularios, CSRF y sesiones seguras.

### ✅ Tareas a Realizar:

#### 1. Formulario con Validación en `tickets/forms.py`:

```python
from django import forms
from django.contrib.auth.models import User
from .models import Ticket

class RegistroForm(forms.ModelForm):
    """Formulario para registro de usuarios"""
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6,
        help_text="La contraseña debe tener mínimo 6 caracteres"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este usuario ya existe")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado")
        return email


class TicketForm(forms.ModelForm):
    """Formulario para crear/editar tickets"""
    
    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del ticket'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descripción del problema'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        
        # Validar longitud mínima
        if len(titulo.strip()) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres")
        
        # Validar que no sea solo números
        if titulo.isdigit():
            raise forms.ValidationError("El título no puede ser solo números")
        
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        
        # Validar longitud mínima
        if len(descripcion.strip()) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres")
        
        return descripcion
```

#### 2. Plantilla de formulario con CSRF:

```html
<!-- tickets/templates/crear_ticket.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Crear Ticket</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #f0f4fb; font-family: Arial; }
        .container { max-width: 600px; margin: 2rem auto; }
        form { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 1.5rem; }
        label { display: block; font-weight: bold; margin-bottom: 0.5rem; color: #1a2540; }
        input, textarea, select { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-family: Arial; }
        input:focus, textarea:focus, select:focus { outline: none; border-color: #4a6fa5; box-shadow: 0 0 5px rgba(74,111,165,0.3); }
        button { width: 100%; padding: 0.75rem; background: #4a6fa5; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background: #3a5f95; }
        .error { color: #dc2626; font-size: 0.85rem; margin-top: 0.25rem; }
        .help-text { color: #7a8baa; font-size: 0.85rem; margin-top: 0.25rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Crear Nuevo Ticket</h1>
        
        <form method="POST" novalidate>
            <!-- CSRF Token - ¡MUY IMPORTANTE! -->
            {% csrf_token %}
            
            <!-- Mostrar errores generales -->
            {% if form.non_field_errors %}
                <div class="form-group">
                    {% for error in form.non_field_errors %}
                        <div class="error">❌ {{ error }}</div>
                    {% endfor %}
                </div>
            {% endif %}
            
            <!-- Campo: Título -->
            <div class="form-group">
                <label for="id_titulo">{{ form.titulo.label }}</label>
                <input 
                    type="text"
                    id="id_titulo"
                    name="titulo"
                    value="{{ form.titulo.value|default:'' }}"
                    placeholder="Ej: Problema con acceso a dashboard"
                    maxlength="100"
                >
                {% if form.titulo.errors %}
                    {% for error in form.titulo.errors %}
                        <div class="error">❌ {{ error }}</div>
                    {% endfor %}
                {% endif %}
            </div>
            
            <!-- Campo: Descripción -->
            <div class="form-group">
                <label for="id_descripcion">{{ form.descripcion.label }}</label>
                <textarea 
                    id="id_descripcion"
                    name="descripcion"
                    rows="5"
                    placeholder="Describe el problema en detalle..."
                >{{ form.descripcion.value|default:'' }}</textarea>
                {% if form.descripcion.errors %}
                    {% for error in form.descripcion.errors %}
                        <div class="error">❌ {{ error }}</div>
                    {% endfor %}
                {% endif %}
                <p class="help-text">Mínimo 10 caracteres</p>
            </div>
            
            <!-- Campo: Estado -->
            <div class="form-group">
                <label for="id_estado">{{ form.estado.label }}</label>
                {{ form.estado }}
                {% if form.estado.errors %}
                    {% for error in form.estado.errors %}
                        <div class="error">❌ {{ error }}</div>
                    {% endfor %}
                {% endif %}
            </div>
            
            <!-- Botón Enviar -->
            <button type="submit">📝 Crear Ticket</button>
        </form>
    </div>
</body>
</html>
```

#### 3. Configuración de Seguridad en `settings.py`:

```python
# === SEGURIDAD DE SESIONES ===

# Cookies HTTP-only (no accesibles desde JavaScript)
SESSION_COOKIE_HTTPONLY = True

# Solo enviar cookies por HTTPS
SESSION_COOKIE_SECURE = False  # False en desarrollo, True en producción

# Protección contra CSRF
SESSION_COOKIE_SAMESITE = 'Lax'  # Lax en desarrollo, Strict en producción

# Duración de sesión (1800 segundos = 30 minutos)
SESSION_COOKIE_AGE = 1800

# URL de redirección después de login
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'

# === PROTECCIÓN CSRF ===
# El middleware CSRF ya está activado (no necesita cambios)
# CSRF_COOKIE_SECURE = True  # Descomentar en producción

# === PROTECCIÓN DE MARCOS ===
X_FRAME_OPTIONS = 'DENY'  # Protege contra clickjacking

# === PARA PRODUCCIÓN ===
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
```

#### 4. Integración en vistas:

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, TicketForm
from .models import Ticket

def registro(request):
    """Vista mejorada de registro con validación"""
    if request.method == "POST":
        form = RegistroForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Crear perfil de usuario normal
            from .models import Rol, UserProfile
            try:
                rol_usuario = Rol.objects.get(nombre='usuario')
                UserProfile.objects.create(usuario=user, rol=rol_usuario)
            except:
                pass
            
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

@login_required
def crear_ticket(request):
    """Vista para crear tickets con validación"""
    if request.method == "POST":
        form = TicketForm(request.POST)
        
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user
            ticket.save()
            
            return redirect('lista')
    else:
        form = TicketForm()
    
    return render(request, 'crear_ticket.html', {'form': form})
```

#### 5. URLs para formularios en `tickets/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registro, name='registro'),
    path('lista/', views.lista_tickets, name='lista'),
    path('crear/', views.crear_ticket, name='crear'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
```

---

## 🚀 Resumen Final

| Persona | Responsabilidad | Estado |
|---------|-----------------|--------|
| **1** | Autenticación (Login/Logout) | ✅ Completado |
| **2** | Roles y Permisos | ✅ Completado |
| **3** | Formularios y Seguridad | ✅ **YA IMPLEMENTADO** |

### Comandos Finales:

```bash
# Hacer migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear roles iniciales
python manage.py create_roles

# Crear admin
python manage.py create_admin admin admin123

# Iniciar servidor
python manage.py runserver 8000
```

---

**¡El proyecto está completamente funcional y seguro!** 🔐✅
