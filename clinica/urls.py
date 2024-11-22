"""
URL configuration for clinica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clinicaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', views.signin, name='signin'),
    path('', views.login_view, name='login'),
    path('home', views.home_view, name='home'),
    path('signout/', views.signout, name='signout'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('pacientesinsert/', views.insertar_pacientes, name='pacientesinsert'),
    path('pacientebusqueda/<nombre>', views.pacientesbusqueda),
    path('pacientebusqueda1/<nombre>', views.pacientesbusqueda1),
    path('pacientebusqueda2/<nombre>', views.pacientesbusqueda2),
    path('pacientebusqueda3/<nombre>', views.pacientesbusqueda3),
    path('medicos/', views.medicos, name='medicos'),
    path('medicosinsert/', views.insertar_medicos, name='medicosinsert'),
    path('medicosbusqueda/<nombre>', views.medicosbusqueda_nombre, ),
    path('medicosbusqueda1/<nombre>', views.medicosbusqueda_apellido, ),
    path('medicosbusqueda2/<nombre>', views.medicosbusqueda_especialidad, ),
    path('medicosbusqueda3/<nombre>', views.medicosbusqueda_telefono),
    path('medicosbusqueda4/<nombre>', views.medicosbusqueda_email, ),
    path('citas/', views.citas, name='citas'),
    path('citasinsert/', views.insertar_citas, name='citasinsert'),
    path('citasbusqueda_nombre/<str:nombre>/', views.citas_busqueda_nombre, name='citasbusqueda_nombre'),
    path('citasbusqueda_apellido/<str:apellido>/', views.citas_busqueda_apellido, name='citasbusqueda_apellido'),
    path('citasbusqueda_nombre1/<str:nombre>/', views.citas_busqueda_nombre1, name='citasbusqueda_nombre1'),
    path('citasbusqueda_apellido2/<str:apellido>/', views.citas_busqueda_apellido2, name='citasbusqueda_apellido2'),
    path('tratamientos/', views.tratamientos, name='tratamientos'),
    path('insertar_tratamiento/', views.insertar_tratamiento, name='insertar_tratamiento'),
    path('tratamientos_busqueda_paciente/<str:nombre>/', views.tratamientos_busqueda_paciente, name='tratamientos_busqueda_paciente'),
    path('tratamientos_busqueda_medico/<str:nombre>/', views.tratamientos_busqueda_medico, name='tratamientos_busqueda_medico'),
    path('redirigir-a-admin/', views.redirigir_a_admin, name='redirigir_a_admin'),
]
