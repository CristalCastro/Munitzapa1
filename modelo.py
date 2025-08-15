from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=200)   
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.user.username
class Dpi

class Ciudadano(models.Model):  # PascalCase corregido
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)  # snake_case corregido
    dpi = models.CharField(max_length=100)
    dpi_imagen = models.ImageField(upload_to='ciudadanos/dpi/', blank=True, null=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Choices definido correctamente
GESTION_STATUS = [
    (1, 'Ingresada'), 
    (2, 'En proceso'), 
    (3, 'Reingreso'), 
    (4, 'Autorizada'), 
    (5, 'Finalizada'), 
    (6, 'Cancelada')
]    

class Gestion(models.Model):  # PascalCase corregido
    title1 = models.CharField(max_length=200)
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)  # Relación mejor
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    departamento_gestion = models.CharField(max_length=100)
    
    # SOLO UN campo de documentos
    documentos = models.FileField(upload_to='documents/', blank=True, null=True)
    
    # Choices corregido - SOLO el número como default
    estado = models.PositiveSmallIntegerField(choices=GESTION_STATUS, default=1)
    
    importante = models.BooleanField(default=False)
    media = models.BooleanField(default=False)
    urgente = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  # Bien indentado
        return self.title1

class Colaborador(models.Model):  # PascalCase corregido
    nombre_colaborador = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)  # Relación corregida
    clave = models.CharField(max_length=20)
    DepartamentoGestion = models.ForeignKey('DepartamentoGestion', on_delete=models.CASCADE)  # Relación corregida

    def __str__(self):
        return self.nombre_colaborador

class DepartamentoGestion(models.Model):  # Sin underscore
    nombre_departamento = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=1000)

    def __str__(self):
        return self.nombre_departamento

