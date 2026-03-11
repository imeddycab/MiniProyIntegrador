# tickets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tickets, name='lista_tickets'),
    path('mis-tickets/', views.mis_tickets, name='mis_tickets'),
    path('crear/', views.crear_ticket, name='crear_ticket'),
    path('editar/<int:ticket_id>/', views.editar_ticket, name='editar_ticket'),
    path('eliminar/<int:ticket_id>/', views.eliminar_ticket, name='eliminar_ticket'),

    # Gestión de usuarios (solo superuser)
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]