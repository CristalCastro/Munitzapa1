from django.forms import ModelForm
from .models import Task, Ciudadano

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'datecompleted']

class ciudadanoForm(ModelForm):
    class Meta:
        model = Ciudadano
        fields = ['id', 'nombre', 'apellido', 'dpi', 'dpi_imagen','telefono','email']
        
        
#class gestionForm(ModelForm):
 #   class Meta:
  #      model =  
   #     fields = ['title1', 'nombre', 'apellido', 'description', 'Departamento_Gestion', 'Documentos', 'Importante', 'Media', 'Urgente', 'documentos']