from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistroForm
from .models import Ticket, UserProfile
from functools import wraps

# Decorador para verificar si es administrador
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if profile.rol and profile.rol.nombre == 'admin':
                    return view_func(request, *args, **kwargs)
            except UserProfile.DoesNotExist:
                pass
        return redirect('login')
    return wrapper

@login_required
def dashboard(request):
    tickets_count = Ticket.objects.filter(usuario=request.user).count()
    context = {
        'tickets_count': tickets_count,
        'user': request.user
    }
    return render(request, 'dashboard.html', context)

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = False
            user.save()
            
            # Crear perfil con rol de usuario normal
            try:
                from .models import Rol
                rol_usuario = Rol.objects.get(nombre='usuario')
                UserProfile.objects.create(usuario=user, rol=rol_usuario)
            except:
                UserProfile.objects.create(usuario=user)
            
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

@login_required
def lista_tickets(request):
    try:
        profile = request.user.profile
        if profile.rol and profile.rol.nombre == 'admin':
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(usuario=request.user)
    except UserProfile.DoesNotExist:
        tickets = Ticket.objects.filter(usuario=request.user)

    return render(request, 'lista.html', {'tickets': tickets})

@admin_required
def admin_panel(request):
    total_usuarios = User.objects.count()
    total_tickets = Ticket.objects.count()
    tickets_abiertos = Ticket.objects.filter(estado='abierto').count()
    tickets_cerrados = Ticket.objects.filter(estado='cerrado').count()
    
    usuarios = User.objects.all()
    tickets = Ticket.objects.all()[:10]  # Últimos 10 tickets
    
    context = {
        'total_usuarios': total_usuarios,
        'total_tickets': total_tickets,
        'tickets_abiertos': tickets_abiertos,
        'tickets_cerrados': tickets_cerrados,
        'usuarios': usuarios,
        'tickets': tickets,
    }
    
    return render(request, 'admin_panel.html', context)