from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('lista/', views.lista_tickets, name='lista'),
    path('registro/', views.registro, name='registro'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]