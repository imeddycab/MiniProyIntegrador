from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tickets, name='lista'),
    path('registro/', views.registro, name='registro'),
]