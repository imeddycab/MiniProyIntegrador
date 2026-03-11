# Formulatio con validacion
from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del ticket'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe el problema...', 'rows': 4}),
        }
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres")
        if len(titulo) > 100:
            raise forms.ValidationError("El título no puede exceder los 100 caracteres")
        return titulo
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres")
        return descripcion