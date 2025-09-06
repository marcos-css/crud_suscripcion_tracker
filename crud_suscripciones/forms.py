from django import forms
from .models import Suscripcion

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ['nombre_servicio', 'costo', 'frecuencia_pago', 'fecha_renovacion', 'activa']
        widgets = {
            'fecha_renovacion': forms.DateInput(attrs={'type': 'date'}),
            'costo': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
