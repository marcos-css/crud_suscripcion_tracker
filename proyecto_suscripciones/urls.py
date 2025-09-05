
from django.contrib import admin
from django.urls import path
from crud_suscripciones.views import inicio
from crud_suscripciones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',inicio, name='inicio'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
]
