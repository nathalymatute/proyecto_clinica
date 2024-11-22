from django.db import models

class Paciente(models.Model):
    id_pacientes = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Medico(models.Model):
    id_medicos = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido} - {self.especialidad}"

class Tratamiento(models.Model):
    id_tratamientos = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    medico_id = models.ForeignKey(Medico, on_delete=models.CASCADE, db_column='medico_id')
    paciente_id = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='paciente_id')

    def __str__(self):
        return f"{self.nombre} - {self.paciente_id}"

class Cita(models.Model):
    id_citas = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    paciente_id = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='paciente_id')
    medico_id = models.ForeignKey(Medico, on_delete=models.CASCADE, db_column='medico_id')

    def __str__(self):
        return f"Cita con {self.medico_id} para {self.paciente_id} el {self.fecha} a las {self.hora}"

