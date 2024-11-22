from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.db import connection
from django.http import HttpResponseServerError
from django.db import transaction
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Paciente, Medico,Tratamiento,Cita
from django.http import JsonResponse


# Create your views here.
def signin(request):
    if request.user.is_authenticated:
        return redirect('/profile')  # Si el usuario ya está autenticado, redirígelo a su perfil
        
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)  # Pasar la solicitud al formulario de autenticación
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Autenticar al usuario
                return redirect('/home')  # Redirigir al usuario a su perfil
            else:
                msg = 'Error: Nombre de usuario o contraseña incorrectos.'
                return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Credenciales inválidas'})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})
@login_required
def home(request):
    return render(request, 'home.html')
@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def home_view(request):

    # Renderiza la plantilla 'home.html' con los datos obtenidos de homeTableM
    return render(request, 'home.html')
@login_required
def signout(request):
    logout(request)
    return redirect('/')

from django.db import connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cita, Paciente, Medico

@login_required
def homeTableCitas(request):
    # Obtener el día, mes y año actuales con la consulta SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT CURDATE() AS fecha_actual")  # Devuelve la fecha completa (día, mes y año)
        fecha_actual = cursor.fetchone()
        if fecha_actual:
            fecha_actual = fecha_actual[0]
            # Desglosamos la fecha actual en día, mes y año
            dia_actual = fecha_actual.day
            mes_actual = fecha_actual.month
            año_actual = fecha_actual.year

    # Obtener las citas para la fecha actual con un INNER JOIN entre Cita, Paciente y Medico
    citas = Cita.objects.raw('''
        SELECT c.id_citas, c.fecha, c.hora, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_cita c
        INNER JOIN clinicaapp_paciente p ON c.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON c.medico_id = m.id_medicos
        WHERE c.fecha = %s
        ORDER BY c.hora
    ''', [fecha_actual])  # Fecha actual obtenida de la consulta SQL

    # Contar el número de citas para el día actual
    conteo_citas = Cita.objects.filter(fecha=fecha_actual).count()

    # Preparar los datos para pasarlos a la plantilla
    citas_data = []
    for cita in citas:
        citas_data.append({
            'id_cita': cita.id_citas,
            'fecha': cita.fecha,
            'hora': cita.hora,
            'paciente_nombre': cita.paciente_nombre,
            'paciente_apellido': cita.paciente_apellido,
            'medico_nombre': cita.medico_nombre,
            'medico_apellido': cita.medico_apellido
        })

    # Retornar los datos a la plantilla
    return citas_data,conteo_citas,fecha_actual,mes_actual,año_actual,dia_actual
 
    

@login_required
def home_view(request):
    # Llamar a homeTableM para obtener los registros de la tabla Balance General

    
    # Llamar al método homeTableCitas para obtener las citas y el conteo de citas
    citas_data, conteo_citas, fecha_actual, mes_actual, año_actual, dia_actual = homeTableCitas(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'conteo_citas': conteo_citas
        })


    # Renderiza la plantilla 'home.html' con todos los datos obtenidos
    return render(request, 'home.html', {
        # Datos de sumaCreditoRenovacion
        'mes': mes_actual,                    # Mes actual
        'año': año_actual,                    # Año actual
        'citas': citas_data,                  # Datos de las citas para hoy
        'conteo_citas': conteo_citas,         # Conteo de citas para hoy
        'fecha_actual': fecha_actual,         # Fecha completa actual
        'dia_actual': dia_actual,             # Día actual
        'mes_actual': mes_actual,             # Mes actual
        'año_actual': año_actual             # Año actual
    })

@login_required
def pacientes(request):
    conteo_citas = Paciente.objects.all().count()
    pacientes = Paciente.objects.all()[:10]
    pacientes_data =[]


    for paciente in pacientes:
        pacientes_data.append({
            'id_pacientes':paciente.id_pacientes,
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            'fecha_nacimiento': paciente.fecha_nacimiento,
            'telefono': paciente.telefono,
            'email': paciente.email

        })

    return render(request, 'pacientes.html',{'pacientes':pacientes_data,

        'conteo_citas': conteo_citas,   })

def pacientesbusqueda(request, nombre):
    pacientes = Paciente.objects.filter(nombre=nombre)
    conteo_citas = Paciente.objects.all().count()
    return render(request, 'pacientes.html', {'pacientes': pacientes,'conteo_citas': conteo_citas})
def pacientesbusqueda1(request, nombre):
    pacientes = Paciente.objects.filter(apellido=nombre)
    conteo_citas = Paciente.objects.all().count()
    return render(request, 'pacientes.html', {'pacientes': pacientes,'conteo_citas': conteo_citas})
def pacientesbusqueda2(request, nombre):
    conteo_citas = Paciente.objects.all().count()
    pacientes = Paciente.objects.filter(telefono=nombre)
    return render(request, 'pacientes.html', {'pacientes': pacientes,'conteo_citas': conteo_citas})
def pacientesbusqueda3(request, nombre):
    conteo_citas = Paciente.objects.all().count()
    pacientes = Paciente.objects.filter(email=nombre)
    return render(request, 'pacientes.html', {'pacientes': pacientes,'conteo_citas': conteo_citas})

# views.py
from django.shortcuts import render, redirect
from .models import Paciente
from django.urls import reverse
from django.utils import timezone

# Vista para listar e insertar pacientes

from datetime import datetime

@login_required
def insertar_pacientes(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.POST.get('nombre').upper()
        apellido = request.POST.get('apellido').upper()
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        # Crear un nuevo paciente
        Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,  # La fecha ya está en el formato correcto
            telefono=telefono,
            email=correo
        )

        return redirect(reverse('pacientes'))

    return render(request, 'pacientes.html')

#medicos
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Medico
from django.contrib.auth.decorators import login_required

# Vista para listar médicos
@login_required
def medicos(request):
    conteo_medicos = Medico.objects.all().count()
    medicos = Medico.objects.all()[:10]
    medicos_data = []

    for medico in medicos:
        medicos_data.append({
            'id_medicos': medico.id_medicos,
            'nombre': medico.nombre,
            'apellido': medico.apellido,
            'especialidad': medico.especialidad,
            'telefono': medico.telefono,
            'email': medico.email,
        })

    return render(request, 'medicos.html', {
        'medicos': medicos_data,
        'conteo_medicos': conteo_medicos,
    })

# Vistas para búsqueda de médicos
def medicosbusqueda_nombre(request, nombre):
    medicos = Medico.objects.filter(nombre__icontains=nombre)
    conteo_medicos = Medico.objects.all().count()
    return render(request, 'medicos.html', {'medicos': medicos,'conteo_medicos': conteo_medicos})

def medicosbusqueda_apellido(request, nombre):
    medicos = Medico.objects.filter(apellido__icontains=nombre)
    conteo_medicos = Medico.objects.all().count()
    return render(request, 'medicos.html', {'medicos': medicos,'conteo_medicos': conteo_medicos})

def medicosbusqueda_especialidad(request, nombre):
    medicos = Medico.objects.filter(especialidad__icontains=nombre)
    conteo_medicos = Medico.objects.all().count()
    return render(request, 'medicos.html', {'medicos': medicos,'conteo_medicos': conteo_medicos})

def medicosbusqueda_telefono(request, nombre):
    medicos = Medico.objects.filter(telefono__icontains=nombre)
    conteo_medicos = Medico.objects.all().count()
    return render(request, 'medicos.html', {'medicos': medicos,'conteo_medicos': conteo_medicos})

def medicosbusqueda_email(request, nombre):
    medicos = Medico.objects.filter(email__icontains=nombre)
    conteo_medicos = Medico.objects.all().count()
    return render(request, 'medicos.html', {'medicos': medicos,'conteo_medicos': conteo_medicos})

# Vista para insertar médicos

@login_required
def insertar_medicos(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.POST.get('nombre').upper()
        apellido = request.POST.get('apellido').upper()
        especialidad = request.POST.get('especialidad').upper()
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')

        # Crear un nuevo médico
        Medico.objects.create(
            nombre=nombre,
            apellido=apellido,
            especialidad=especialidad,
            telefono=telefono,
            email=email
        )

        return redirect(reverse('medicos'))

    return render(request, 'medicos.html')

from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from django.contrib.auth.decorators import login_required
from .models import Cita, Paciente, Medico

# Vista para listar las citas del día actual
from django.db import connection
from django.shortcuts import render
from .models import Cita, Medico

@login_required
def citas(request):
    # Obtener la fecha actual
    with connection.cursor() as cursor:
        cursor.execute("SELECT CURDATE() AS fecha_actual")
        fecha_actual = cursor.fetchone()[0]

    # Obtener las citas del día actual
    citas = Cita.objects.raw('''
        SELECT c.id_citas, c.fecha, c.hora, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_cita c
        INNER JOIN clinicaapp_paciente p ON c.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON c.medico_id = m.id_medicos
        WHERE c.fecha = %s
        ORDER BY c.hora
    ''', [fecha_actual])

    # Contar el número de citas del día
    conteo_citas = Cita.objects.filter(fecha=fecha_actual).count()

    # Obtener los médicos para llenar el combobox
    medicos = Medico.objects.all()

    # Preparar los datos de las citas para la plantilla
    citas_data = []
    for cita in citas:
        citas_data.append({
            'id_cita': cita.id_citas,
            'fecha': cita.fecha,
            'hora': cita.hora,
            'paciente_nombre': cita.paciente_nombre,
            'paciente_apellido': cita.paciente_apellido,
            'medico_nombre': cita.medico_nombre,
            'medico_apellido': cita.medico_apellido,
        })

    # Pasar los médicos y citas al contexto
    return render(request, 'citas.html', {
        'citas': citas_data,
        'conteo_citas': conteo_citas,
        'medicos': medicos,  # Lista de médicos para el combobox
    })


# Vistas para buscar citas por nombre o apellido del paciente
# Vista para la búsqueda de citas por nombre del paciente
def citas_busqueda_nombre(request, nombre):
    citas = Cita.objects.raw('''
        SELECT c.id_citas, c.fecha, c.hora, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_cita c
        INNER JOIN clinicaapp_paciente p ON c.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON c.medico_id = m.id_medicos
        WHERE p.nombre LIKE %s AND c.fecha = CURDATE()
        ORDER BY c.hora
    ''', [f'%{nombre}%'])
    medicos = Medico.objects.all()


    return render(request, 'citas.html', {'citas': citas,'medicos': medicos, 'conteo_citas': len(citas)})

# Vista para la búsqueda de citas por apellido del paciente
def citas_busqueda_apellido(request, apellido):
    citas = Cita.objects.raw('''
        SELECT c.id_citas, c.fecha, c.hora, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_cita c
        INNER JOIN clinicaapp_paciente p ON c.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON c.medico_id = m.id_medicos
        WHERE p.apellido LIKE %s AND c.fecha = CURDATE()
        ORDER BY c.hora
    ''', [f'%{apellido}%'])
    medicos = Medico.objects.all()

    return render(request, 'citas.html', {'citas': citas,'medicos': medicos, 'conteo_citas': len(citas)})


# Vista para insertar nuevas citas
@login_required
def insertar_citas(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        medico_id = request.POST.get('medico_id')
        paciente_email = request.POST.get('paciente_email')

        # Validar que el correo electrónico del paciente exista en la base de datos
        try:
            paciente = Paciente.objects.get(email=paciente_email)
        except Paciente.DoesNotExist:
            return render(request, 'insertar_citas.html', {
                'error': 'El correo electrónico proporcionado no está registrado.',
                'medicos': Medico.objects.all(),
                'pacientes': Paciente.objects.all()
            })

        # Crear una nueva cita
        Cita.objects.create(
            fecha=fecha,
            hora=hora,
            medico_id_id=medico_id,
            paciente_id_id=paciente.id_pacientes
        )

        return redirect(reverse('citas'))

    # Obtener la lista de pacientes y médicos para los combos
    medicos = Medico.objects.all()

    return render(request, 'insertar_citas.html', {
        'medicos': medicos
    })
def citas_busqueda_nombre1(request, nombre):
    citas = Cita.objects.raw('''
        SELECT c.id_citas, c.fecha, c.hora, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_cita c
        INNER JOIN clinicaapp_paciente p ON c.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON c.medico_id = m.id_medicos
        WHERE m.nombre LIKE %s AND c.fecha = CURDATE()
        ORDER BY c.hora
    ''', [f'%{nombre}%'])
    medicos = Medico.objects.all()


    return render(request, 'citas.html', {'citas': citas,'medicos': medicos, 'conteo_citas': len(citas)})

# Vista para la búsqueda de citas por apellido del paciente
def citas_busqueda_apellido2(request, apellido):
    citas = Cita.objects.raw('''
        SELECT c.id_citas, c.fecha, c.hora, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_cita c
        INNER JOIN clinicaapp_paciente p ON c.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON c.medico_id = m.id_medicos
        WHERE m.apellido LIKE %s AND c.fecha = CURDATE()
        ORDER BY c.hora
    ''', [f'%{apellido}%'])
    medicos = Medico.objects.all()

    return render(request, 'citas.html', {'citas': citas,'medicos': medicos, 'conteo_citas': len(citas)})

from django.shortcuts import render, redirect
from .models import Tratamiento, Medico, Paciente
from django.db import connection
from django.contrib.auth.decorators import login_required

# Vista para mostrar todos los tratamientos
@login_required
def tratamientos(request):
    # Obtener todos los tratamientos
    tratamientos = Tratamiento.objects.raw('''
        SELECT t.id_tratamientos, t.nombre AS tratamiento_nombre, t.descripcion, 
               p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_tratamiento t
        INNER JOIN clinicaapp_paciente p ON t.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON t.medico_id = m.id_medicos
    ''')

    # Obtener los médicos para llenar el combobox
    medicos = Medico.objects.all()

    # Preparar los datos de los tratamientos para la plantilla
    tratamientos_data = []
    for tratamiento in tratamientos:
        tratamientos_data.append({
            'id_tratamiento': tratamiento.id_tratamientos,
            'tratamiento_nombre': tratamiento.tratamiento_nombre,
            'descripcion': tratamiento.descripcion,
            'paciente_nombre': tratamiento.paciente_nombre,
            'paciente_apellido': tratamiento.paciente_apellido,
            'medico_nombre': tratamiento.medico_nombre,
            'medico_apellido': tratamiento.medico_apellido,
        })

    # Pasar los médicos y tratamientos al contexto
    return render(request, 'tratamientos.html', {
        'tratamientos': tratamientos_data,
        'medicos': medicos,  # Lista de médicos para el combobox
    })

# Vista para la búsqueda de tratamientos por nombre del paciente
def tratamientos_busqueda_paciente(request, nombre):
    tratamientos = Tratamiento.objects.raw('''
        SELECT t.id_tratamientos, t.nombre AS tratamiento_nombre, t.descripcion, 
               p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_tratamiento t
        INNER JOIN clinicaapp_paciente p ON t.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON t.medico_id = m.id_medicos
        WHERE p.nombre LIKE %s
    ''', [f'%{nombre}%'])
    
    medicos = Medico.objects.all()

    return render(request, 'tratamientos.html', {'tratamientos': tratamientos, 'medicos': medicos, 'conteo_tratamientos': len(tratamientos)})

# Vista para la búsqueda de tratamientos por nombre del médico
def tratamientos_busqueda_medico(request, nombre):
    tratamientos = Tratamiento.objects.raw('''
        SELECT t.id_tratamientos, t.nombre AS tratamiento_nombre, t.descripcion, 
               p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
               m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM clinicaapp_tratamiento t
        INNER JOIN clinicaapp_paciente p ON t.paciente_id = p.id_pacientes
        INNER JOIN clinicaapp_medico m ON t.medico_id = m.id_medicos
        WHERE m.nombre LIKE %s
    ''', [f'%{nombre}%'])

    medicos = Medico.objects.all()

    return render(request, 'tratamientos.html', {'tratamientos': tratamientos, 'medicos': medicos, 'conteo_tratamientos': len(tratamientos)})

@login_required
def insertar_tratamiento(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        tratamiento_nombre = request.POST.get('tratamiento_nombre')
        descripcion = request.POST.get('descripcion')
        medico_id = request.POST.get('medico_id')
        paciente_email = request.POST.get('paciente_email')

        # Validar que el correo electrónico del paciente exista en la base de datos
        try:
            paciente = Paciente.objects.get(email=paciente_email)
        except Paciente.DoesNotExist:
            return render(request, 'tratamientos.html', {
                'error': 'El correo electrónico proporcionado no está registrado.',
                'medicos': Medico.objects.all(),
                'tratamientos': Tratamiento.objects.all()  # Mostrar los tratamientos ya existentes
            })

        # Crear un nuevo tratamiento
        Tratamiento.objects.create(
            nombre=tratamiento_nombre,
            descripcion=descripcion,
            medico_id_id=medico_id,
            paciente_id_id=paciente.id_pacientes
        )

        # Redirigir a la página de tratamientos después de insertar
        return redirect(reverse('tratamientos'))

    # Obtener la lista de médicos para los combos
    medicos = Medico.objects.all()

    return render(request, 'tratamientos.html', {
        'medicos': medicos
    })

@login_required
def redirigir_a_admin(request):
    # Redirige al usuario a la página de administración
    return redirect('admin:index')


