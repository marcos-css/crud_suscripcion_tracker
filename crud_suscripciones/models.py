from django.db import models
from django.contrib.auth.models import User

class Suscripcion(models.Model):
    FRECUENCIAS = [
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
        ('trimestral', 'Trimestral'),
        ('semanal', 'Semanal'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_servicio = models.CharField(max_length=100)  # Netflix, Spotify, etc.
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    frecuencia_pago = models.CharField(max_length=20, choices=FRECUENCIAS)
    fecha_renovacion = models.DateField()
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha_renovacion']

    def __str__(self):
        return f"{self.nombre_servicio} - ${self.costo}"
    
    def dias_hasta_renovacion(self):
        from datetime import date
        return (self.fecha_renovacion - date.today()).days
    
class ConfiguracionNotificacion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    dias_aviso = models.IntegerField(default=3)
    email_notificaciones = models.EmailField(blank=True)
    activa = models.BooleanField(default=True)