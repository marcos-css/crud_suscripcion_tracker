from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Suscripcion

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
        
