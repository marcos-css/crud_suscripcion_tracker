from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Suscripcion
from django.contrib.auth.decorators import login_required
from .forms import SuscripcionForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Suscripcion, ConfiguracionNotificacion


# Create your views here.
def inicio(request):
    if request.user.is_authenticated:
        # Mostrar suscripciones del usuario
        suscripciones = Suscripcion.objects.filter(
            usuario=request.user, 
            activa=True
        ).order_by('fecha_renovacion')
        
        # Calcular gasto mensual
        total_mensual = 0
        for sus in suscripciones:
            if sus.frecuencia_pago == 'mensual':
                total_mensual += sus.costo
            elif sus.frecuencia_pago == 'anual':
                total_mensual += sus.costo / 12
            elif sus.frecuencia_pago == 'trimestral':
                total_mensual += sus.costo / 3
            elif sus.frecuencia_pago == 'semanal':
                total_mensual += sus.costo * 4
        
        context = {
            'suscripciones': suscripciones,
            'total_suscripciones': suscripciones.count(),
            'gasto_mensual': round(total_mensual, 2),
            'gasto_anual': round(total_mensual * 12, 2),
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save() 
                login(request, user)
                return redirect('/')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Contrasenas no coinciden'
        })
    
def signout(request):
    logout(request)
    return redirect('/')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user=authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'el usuario o contrasena es incorrecta'
        })
        else:
            login(request, user)
            return redirect('/')
        

def crear_suscripcion(request):
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            nueva_sus = form.save(commit=False)
            nueva_sus.usuario = request.user
            nueva_sus.save()
            return redirect('inicio')  # vuelve a la lista de suscripciones
    else:
        form = SuscripcionForm()
    return render(request, 'crear_suscripcion.html', {'form': form})

@login_required
def editar_suscripcion(request, id):
    # Obtener la suscripción del usuario actual
    suscripcion = get_object_or_404(Suscripcion, id=id, usuario=request.user)
    
    if request.method == 'GET':
        # Mostrar formulario con datos actuales
        initial_data = {
            'nombre_servicio': suscripcion.nombre_servicio,
            'costo': suscripcion.costo,
            'frecuencia_pago': suscripcion.frecuencia_pago,
            'fecha_renovacion': suscripcion.fecha_renovacion
        }
        return render(request, 'editar_suscripcion.html', {
            'suscripcion': suscripcion,
            'initial_data': initial_data
        })
    else:
        # Procesar el formulario enviado
        try:
            suscripcion.nombre_servicio = request.POST['nombre_servicio']
            suscripcion.costo = float(request.POST['costo'])
            suscripcion.frecuencia_pago = request.POST['frecuencia_pago']
            suscripcion.fecha_renovacion = request.POST['fecha_renovacion']
            suscripcion.save()
            
            return redirect('/')  # Regresar a inicio tras editar
        except:
            return render(request, 'editar_suscripcion.html', {
                'suscripcion': suscripcion,
                'error': 'Error al actualizar la suscripción'
            })

@login_required
def configurar_notificaciones(request):
    # Obtener o crear configuración del usuario
    config, created = ConfiguracionNotificacion.objects.get_or_create(
        usuario=request.user,
        defaults={
            'dias_aviso': 3, 
            'activa': True,
            'email_notificaciones': request.user.email  # Email por defecto
        }
    )
    
    if request.method == 'GET':
        return render(request, 'configurar_notificaciones.html', {
            'config': config
        })
    else:
        try:
            config.dias_aviso = int(request.POST['dias_aviso'])
            config.email_notificaciones = request.POST['email_notificaciones']
            config.activa = 'activa' in request.POST
            config.save()
            
            return render(request, 'configurar_notificaciones.html', {
                'config': config,
                'mensaje': 'Configuración guardada exitosamente'
            })
        except:
            return render(request, 'configurar_notificaciones.html', {
                'config': config,
                'error': 'Error al guardar la configuración'
            })