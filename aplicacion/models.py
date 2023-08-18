from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
from django.utils import timezone
from datetime import time


class ConsultasModel (models.Model):
    cnombre = models.CharField(max_length=30,name="cnombre")
    capellido = models.CharField(max_length=30,name="capellido")
    cemail = models.EmailField(default="example@example.com",name="cemail")
    cconsulta = models.TextField(max_length=500,name="cconsulta")

    def __str__(self):
        return f"{self.cnombre}, {self.capellido}, {self.cemail}, {self.cconsulta} "



class PerfilPaciente(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=30)

    apellido = models.CharField(max_length=30)

    email = models.EmailField(blank=True,unique=True,null=False)

    whatsapp = models.CharField (blank=True,max_length=14)
    
    def __str__(self):
        return f"{self.nombre}, {self.apellido} "



class Historia_ClinicaModel(models.Model):
    
    perfil_paciente = models.OneToOneField(PerfilPaciente, on_delete=models.CASCADE, primary_key=True)
    
    patologias = models.BooleanField(default=False,null=True,blank=True)

    enfermedades_respiratorias = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.perfil_paciente.nombre}, {self.perfil_paciente.apellido}"
    

    



    
class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.user} [{self.imagen}]"