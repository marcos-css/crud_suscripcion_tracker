from django import forms
from .models import Suscripcion

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ['nombre_servicio', 'costo', 'frecuencia_pago', 'fecha_renovacion', 'activa']
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'frecuencia_pago': forms.Select(attrs={'class': 'form-select'}),
            'fecha_renovacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
