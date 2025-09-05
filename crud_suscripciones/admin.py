from django.contrib import admin
from .models import Suscripcion, ConfiguracionNotificacion

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['nombre_servicio', 'usuario', 'costo', 'frecuencia_pago', 'fecha_renovacion', 'activa']
    list_filter = ['frecuencia_pago', 'activa']
    search_fields = ['nombre_servicio', 'usuario__username']

@admin.register(ConfiguracionNotificacion)
class ConfiguracionNotificacionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'dias_aviso', 'activa']