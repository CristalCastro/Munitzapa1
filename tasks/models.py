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

class Gestion(models.Model):  # PascalCase corregido
    numero_gestion = models.CharField(max_length=50, unique=True)  # Corregido a CharField y único
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

    def __str__(self):  
        return  "{self.numero_gestion},{Ciudadano} - {self.get_estado_display()}"
    

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

class Colaborador(models.Model):  
    dpi_colaborador = models.CharField(max_length=13, unique=True)
    nombre_colaborador = models.CharField(max_length=100)
    #clave = models.CharField(max_length=20)
    #departamento_gestion = models.ForeignKey('DepartamentoGestion', on_delete=models.CASCADE)  # Relación corregida
    departamento_gestion =models.PositiveSmallIntegerField(choices= DEPARTAMENTOS, default=1)
    correo_colaborador = models.EmailField(max_length=100)
    correo_colaborador_validator = RegexValidator(
       regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
       message="Ingrese una dirección de correo electrónico válida.",
       code="invalid_email"
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
    #clave_colaborador = models.CharField(max_length=10, unique=True, blank=True)

    #def save(self, *args, **kwargs):
     #   if not self.clave_colaborador:
      #      # Obtener el último ID y generar el código
       #     ultimo_id = Colaborador.objects.all().count() + 1
        #    self.clave_colaborador = f'COL{ultimo_id:03d}'  # Ejemplo: EMP001, EMP002
        #super().save(*args, **kwargs)

    #def __str__(self):
     #   return f'{self.nombre_colaborador} ({self.clave_colaborador})'
    

    #def __str__(self):
     #   return self.nombre_colaborador
    clave_colaborador = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.clave_colaborador:
            prefijo = self.departamento_gestion.upper()

            # Buscar la última clave generada para este departamento
            ultimo = Colaborador.objects.filter(
                departamento=self.departamento_gestion,
                clave_colaborador__startswith=prefijo
            ).order_by('-clave_colaborador').first()

            if ultimo:
                import re
                match = re.search(rf'{prefijo}(\d+)', ultimo.clave_colaborador)
                numero = int(match.group(1)) + 1 if match else 1
            else:
                numero = 1

            # Generar nueva clave
            self.clave_colaborador = f'{prefijo}{numero:03d}'

        super().save(*args, **kwargs)

   
    def __str__(self):
        return f'{self.nombre_colaborador} ({self.clave_colaborador})'
    

class DepartamentoGestion(models.Model):  
    #nombre_departamento = models.CharField(max_length=100)
    nombre_departamento = models.PositiveSmallIntegerField(choices=DEPARTAMENTOS, default=1)
    Colaborador_responsable = models.ForeignKey(Colaborador, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField(max_length=1000)
    def __str__(self):
        return self.nombre_departamento

def generar_numero():
    fecha = now().strftime("%Y%m%d")
    ultimo = Solicitud_gestion.objects.filter(fecha__date=now().date()).count() + 1
    return f"SOL-{fecha}-{ultimo:03d}"



class Solicitud_gestion(models.Model): 
    numero_solicitud = models.CharField(max_length=20, default=generar_numero, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)   
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    estado = models.PositiveSmallIntegerField(choices=GESTION_STATUS, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Solicitud de {self.ciudadano} - Estado: {self.get_GESTION_STATUS_display()}"


