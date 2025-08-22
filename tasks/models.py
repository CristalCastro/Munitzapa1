from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.timezone import now
import re

class Task(models.Model):
    title = models.CharField(max_length=200)   
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.user.username

ESTADOS_CIVIL= [
    (1, 'Soltero/a'), 
    (2, 'casado/a'), 
    (3, 'Divorciado/a'), 
    (4, 'viudo/a'), 
    (5, 'union libre'), 
]  
GENEROS = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]    
DEPARTAMENTOS= [
    ('AM','Alcaldía Municipal'), 
    ('DAFIM', 'Departamento de Finanzas'), 
    ('SG', 'Secretaría General'), 
    ('RC', 'Recepción'), 
    ('DMP', 'DMP'),
    ('DMM', 'DMM'), 
    ('OMNAP', 'OMNAP'), 
    ('RH', 'RECURSOS HUMANOS'), 
    ('CT', 'CONTABILIDAD'), 
    ('CP', 'COMPRAS'), 
]
class Ciudadano(models.Model):  # PascalCase corregido
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)  # snake_case corregido
    dpi = models.CharField(
        max_length=13,
        validators=[RegexValidator(
            regex=r'^\d{13}$',
            message='Ingrese un DPI válido de 13 dígitos.',
            code='invalid_dpi',
        )]
    )
    dpi_imagen = models.ImageField(upload_to='ciudadanos/dpi/', blank=True, null=True)
    genero = models.CharField(max_length=1, choices=GENEROS, verbose_name="Género")
    Estado_civil = models.PositiveSmallIntegerField(choices=ESTADOS_CIVIL, default=1)
    telefono = models.CharField(
           max_length=20,
           validators=[
               RegexValidator(
                   regex=r'^\+?1?\d{8}$',
                   message="El número de teléfono debe tener un formato válido.",
               )
           ]    
       )
    email = models.EmailField(max_length=100)
    email_validator = RegexValidator(
       regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
       message="Ingrese una dirección de correo electrónico válida.",
       code="invalid_email"
   )
    
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

class Gestion(models.Model):  
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)  # Relación mejor
    description = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    departamento_gestion =models.CharField(choices= DEPARTAMENTOS, default= 'AM', max_length=10)  # Corregido el campo de departamento
    
    # SOLO UN campo de documentos
    documentos = models.FileField(upload_to='documents/', blank=True, null=True)
    
    # Choices corregido - SOLO el número como default
    estado = models.PositiveSmallIntegerField(choices=GESTION_STATUS, default=1)
    importante = models.BooleanField(default=False)
    media = models.BooleanField(default=False)
    urgente = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

        
    def __str__(self):
        return f"{self.ciudadano} {self.estado}"


def generar_clave(departamento_codigo):
    fecha = now().strftime("%Y%m%d")
    # Importar aquí para evitar importación circular
    from .models import Colaborador  # Ajusta la importación según tu estructura
    
    
# Contador global independiente del departamento
    contador = Colaborador.objects.filter(
        fecha__date=now().date()
    ).count() + 1
    return f"{departamento_codigo}-{fecha}-{contador:03d}"

class Colaborador(models.Model):  
    dpi_colaborador = models.CharField(max_length=13, unique=True)
    nombre_colaborador = models.CharField(max_length=100)
    genero = models.CharField(max_length=1, choices=GENEROS, verbose_name="Género")
    Estado_civil = models.PositiveSmallIntegerField(choices=ESTADOS_CIVIL, default=1)
    departamento_gestion = models.CharField(max_length=10, choices=DEPARTAMENTOS, default='AM')
    
    # Validador aplicado correctamente al campo
    correo_colaborador = models.EmailField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message="Ingrese una dirección de correo electrónico válida.",
                code="invalid_email"
            )
        ]
    )
    
    telefono_colaborador = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{8}$',
                message="El número de teléfono debe tener un formato válido.",
            )
        ]
    )
    
    fecha = models.DateTimeField(auto_now_add=True) 
    clave_colaborador = models.CharField(max_length=20, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.clave_colaborador:
            self.clave_colaborador = generar_clave(self.departamento_gestion)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_colaborador} - {self.clave_colaborador}"

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"


class DepartamentoGestion(models.Model):  
    nombre_departamento = models.CharField(max_length=10, choices=DEPARTAMENTOS, default='AM')
    Colaborador_responsable = models.ForeignKey(Colaborador, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.nombre_departamento

def generar_numero():
    fecha = now().strftime("%Y%m%d")
    ultimo = Solicitud_gestion.objects.filter(fecha__date=now().date()).count() + 1
    return f"SOL-{fecha}-{ultimo:03d}"

TIPO_SOL = [
    (1, 'Solicitud de Agua'), 
    (2, 'Solicitud Drenaje'), 
    (3, 'Solicitud de Alumbrado'), 
    (4, 'Solicitud de Ayuda Social'), 
    (5, 'Solicitud de Mantenimiento'),
    (6, 'Solicitud de Certificación'),
    (7, 'Solicitud de Permiso'), 
    (8, 'Solicitud de Información'),
    (9, 'Solicitud de Queja'),  
    (10,'Solicitud de carta de Residencia'),
    (11,'Solicitud de procesos Jurídicos'),
    (12,'Solicitud de Certificación de Nichos'),
    (13,'Solicitud de Certificación de Propiedad'),
    (14,'Solicitud de Donaciones'),
    (15,'Solicitud de Licencia de Funcionamiento'),
    (16,'Solicitud de Limpieza de calles'),
    (17,'Solicitud de Mantenimiento de Agua Xepacay'),
    (18,'Solicitud de Mantenimiento de Parques'),
    (19,'Solicitud de Mantenimiento de Cementerio'),
    (20,'Solicitud de Donaciones de Arboles'),
    (21,'Solicitud de Actividades Culturales'),
    (22,'Solicitud de Actividades Deportivas'),
    (23,'Solicitud de Actividades Recreativas'),
    (24,'Solicitud de Actividades Educativas'),
    (25,'Solicitud de Actividades Sociales'),
    (26,'Solicitud de Actividades Económicas'),
    (27,'Solicitud de Actividades Ambientales'),
    (28,'Solicitud de Actividades de Salud'),
    (29,'Solicitud de Actividades de Seguridad'),
    (30,'Solicitud de Actividades de Infraestructura'),
    (31,'Solicitud de Actividades de Actividades de Ferias'),
    (32,'Solicitud de Control Fontanería'),
    (33,'Solicitud de Alquiler de Espacios Públicos'),
    (34,'Solicitud de Alquiler de Salones'),    
    (35,'Otros')
]    
class TipoSolicitud(models.Model):
    Tipo_solicitud = models.IntegerField(choices=TIPO_SOL, default=1)
    descripcion = models.TextField(blank=True)
    DepartamentoGestion = models.ForeignKey(DepartamentoGestion, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.Tipo_solicitud}"
    
class Solicitud_gestion(models.Model): 
    numero_solicitud = models.CharField(max_length=20, default=generar_numero, unique=True)
    Tipo_solicitud = models.IntegerField(choices=TIPO_SOL, default=1)
    fecha = models.DateTimeField(auto_now_add=True)   
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=100)
    #gestion= models.ForeignKey(Gestion, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    estado = models.PositiveSmallIntegerField(choices=GESTION_STATUS, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self):
         return f"{self.numero_solicitud} - {self.Tipo_solicitud} - {self.ciudadano.nombre} {self.ciudadano.apellido}"

