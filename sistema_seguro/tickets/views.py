from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistroForm
from .models import Ticket

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            # usuario normal
            user.is_staff = False

            user.save()
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

@login_required
def lista_tickets(request):

    if request.user.is_staff:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(usuario=request.user)

    return render(request, 'lista.html', {'tickets': tickets})