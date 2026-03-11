# tickets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Ticket
from .forms import TicketForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

@login_required
def lista_tickets(request):
    """Vista principal con diferenciación de roles"""
    if request.user.is_staff:
        # Admin ve todos los tickets
        tickets = Ticket.objects.all()
        # Calcula usuarios activos (con tickets)
        usuarios_activos = User.objects.filter(tickets__isnull=False).distinct().count()
    else:
        # Usuario normal solo ve sus tickets
        tickets = Ticket.objects.filter(usuario=request.user)
        usuarios_activos = 1  # Solo el usuario actual
    
    context = {
        'tickets': tickets,
        'total_tickets': tickets.count(),
        'usuarios_activos': usuarios_activos,
        'es_admin': request.user.is_staff
    }
    return render(request, 'lista.html', context)

@login_required
def crear_ticket(request):
    """Crear ticket (accesible para ambos roles)"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user
            ticket.save()
            messages.success(request, '✅ Ticket creado exitosamente!')
            return redirect('lista_tickets')
    else:
        form = TicketForm()
    
    return render(request, 'ticket_form.html', {
        'form': form, 
        'accion': 'Crear',
        'es_admin': request.user.is_staff
    })

@login_required
def editar_ticket(request, ticket_id):
    """Editar ticket con verificación de permisos"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Verificar permisos
    if not request.user.is_staff and ticket.usuario != request.user:
        messages.error(request, '⛔ No tienes permiso para editar este ticket')
        return redirect('lista_tickets')
    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Ticket actualizado exitosamente!')
            return redirect('lista_tickets')
    else:
        form = TicketForm(instance=ticket)
    
    return render(request, 'ticket_form.html', {
        'form': form, 
        'accion': 'Editar',
        'es_admin': request.user.is_staff
    })

@login_required
def eliminar_ticket(request, ticket_id):
    """Eliminar ticket (solo admin)"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Solo admin puede eliminar
    if not request.user.is_staff:
        messages.error(request, '⛔ Solo los administradores pueden eliminar tickets')
        return redirect('lista_tickets')
    
    if request.method == 'POST':
        titulo = ticket.titulo
        ticket.delete()
        messages.success(request, f'✅ Ticket "{titulo}" eliminado')
        return redirect('lista_tickets')
    
    return render(request, 'confirmar_eliminar.html', {
        'ticket': ticket,
        'es_admin': request.user.is_staff
    })

@login_required
def mis_tickets(request):
    """Vista específica para ver solo mis tickets"""
    tickets = Ticket.objects.filter(usuario=request.user)
    return render(request, 'lista.html', {
        'tickets': tickets,
        'titulo': 'Mis Tickets',
        'es_admin': request.user.is_staff
    })

@login_required
def lista_usuarios(request):
    """Solo superuser puede ver lista de usuarios"""
    if not request.user.is_superuser:
        messages.error(request, '⛔ Acceso denegado. Solo administradores.')
        return redirect('lista_tickets')
    
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'lista_usuarios.html', {
        'usuarios': usuarios,
        'total_usuarios': usuarios.count(),
        'activos': usuarios.filter(is_active=True).count(),
        'staff': usuarios.filter(is_staff=True).count()
    })

@login_required
def crear_usuario(request):
    """Solo superuser puede crear usuarios"""
    if not request.user.is_superuser:
        messages.error(request, '⛔ Acceso denegado.')
        return redirect('lista_tickets')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        
        # Validaciones
        if not username or not password:
            messages.error(request, 'Usuario y contraseña son obligatorios')
            return render(request, 'usuario_form.html')
        
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'usuario_form.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return render(request, 'usuario_form.html')
        
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'usuario_form.html')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_active=is_active
        )
        
        messages.success(request, f'✅ Usuario {username} creado exitosamente')
        return redirect('lista_usuarios')
    
    return render(request, 'usuario_form.html', {'accion': 'Crear'})

@login_required
def editar_usuario(request, user_id):
    """Solo superuser puede editar usuarios"""
    if not request.user.is_superuser:
        messages.error(request, '⛔ Acceso denegado.')
        return redirect('lista_tickets')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        new_password = request.POST.get('new_password')
        
        # Validar username único (excepto el mismo)
        if User.objects.exclude(id=user_id).filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return render(request, 'usuario_form.html', {'usuario': user, 'accion': 'Editar'})
        
        # Actualizar datos
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.is_active = is_active
        
        # Si se proporcionó nueva contraseña
        if new_password:
            user.set_password(new_password)
        
        user.save()
        
        messages.success(request, f'✅ Usuario {username} actualizado')
        return redirect('lista_usuarios')
    
    return render(request, 'usuario_form.html', {
        'usuario': user,
        'accion': 'Editar'
    })

@login_required
def eliminar_usuario(request, user_id):
    """Solo superuser puede eliminar usuarios"""
    if not request.user.is_superuser:
        messages.error(request, '⛔ Acceso denegado.')
        return redirect('lista_tickets')
    
    user = get_object_or_404(User, id=user_id)
    
    # No permitir eliminarse a sí mismo
    if user.id == request.user.id:
        messages.error(request, '⛔ No puedes eliminarte a ti mismo')
        return redirect('lista_usuarios')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'✅ Usuario {username} eliminado')
        return redirect('lista_usuarios')
    
    return render(request, 'confirmar_eliminar_usuario.html', {'usuario': user})