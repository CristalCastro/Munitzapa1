from django.contrib import admin
from .models import Task, Ciudadano, Gestion, Colaborador, DepartamentoGestion, Solicitud_gestion

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'important', 'created']  # Usar 'important' (campo en inglés)
    list_filter = ['important', 'created']

@admin.register(Ciudadano)
class CiudadanoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'dpi', 'telefono', 'email']
    search_fields = ['nombre', 'apellido', 'dpi']

@admin.register(Gestion)
class GestionAdmin(admin.ModelAdmin):
    list_display = ['ciudadano', 'estado', 'created']
    list_filter = ['estado', 'importante', 'urgente', 'created']
    readonly_fields = ['created']
    search_fields = ['ciudadano__nombre', 'ciudadano__apellido']

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    # CORREGIDO: 'departamento_gestion' no 'Departamento_Gestion'
    list_display = ['nombre_colaborador', 'clave_colaborador', 'departamento_gestion']
    list_filter = ['departamento_gestion']

@admin.register(DepartamentoGestion)
class DepartamentoGestionAdmin(admin.ModelAdmin):
    list_display = ['nombre_departamento', 'descripcion']
    search_fields = ['nombre_departamento']

@admin.register(Solicitud_gestion)
class SolicitudGestionAdmin(admin.ModelAdmin):
    list_display = ['ciudadano', 'descripcion', 'estado', 'created']
    list_filter = ['estado']
    search_fields = ['ciudadano__nombre', 'descripcion']


