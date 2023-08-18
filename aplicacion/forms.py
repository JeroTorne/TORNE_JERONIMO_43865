from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import *





class ConsultasForm(forms.Form):
    cnombre = forms.CharField(label="Nombre",max_length=20,required=True)
    capellido = forms.CharField(label="Apellido",max_length=20,required=True)
    cemail = forms.EmailField(label="Email", required=True)
    cconsulta = forms.CharField(label="Consulta",required=True,widget=forms.Textarea(attrs={"rows":"","cols":""}))






class RegistroPacientesForm(UserCreationForm):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Email Usuario")
    password1= forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2= forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}





class EditarUsuario(UserCreationForm):
    email = forms.EmailField(label="Modificar E-mail",required=False)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput,required=False)
    password2 = forms.CharField(label='Repetir la contraseña', widget=forms.PasswordInput,required=False) 
    first_name = forms.CharField(label="Nombre/s", max_length=50, required=False)
    last_name = forms.CharField(label="Apellido/s", max_length=50, required=False)
    imagen = forms.ImageField(required=False,label="Foto de perfil") 
    class Meta:
        model = User
        fields = [ 'email', 'password1', 'password2', 'first_name', 'last_name' ] 
        #Saca los mensajes de ayuda
        help_texts = { k:"" for k in fields}






# class HistoriaClinica(UserCreationForm):

#     first_name = forms.CharField(label="Nombre/s", max_length=50, required=False)
#     last_name = forms.CharField(label="Apellido/s", max_length=50, required=False)
#     patologias = forms.BooleanField(required=False)
#     enfermedades_respiratorias = forms.BooleanField(required=False)
#     email = forms.EmailField(label="Modificar E-mail",required=False)
#     password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput,required=False)
#     password2 = forms.CharField(label='Repetir la contraseña', widget=forms.PasswordInput,required=False)
#     class Meta:
#         model = Historia_ClinicaModel
#         fields = ['perfil_paciente','patologias','enfermedades_respiratorias']  # Incluye otros campos aquí si es necesario

#         widgets = {
#             'enfermedades_respiratorias': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'patologias': forms.CheckboxInput(attrs={'class': 'form-check-input'})
#         }
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.fields['nombre'] = forms.CharField(max_length=30, initial=self.instance.perfil_paciente.nombre)
            
#     class Meta:
#         model = User
#         fields = [ 'first_name', 'last_name','email', 'password1', 'password2' ] 
#         #Saca los mensajes de ayuda
#         help_texts = { k:"" for k in fields}
    

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = Historia_ClinicaModel
        fields = ['perfil_paciente', 'patologias', 'enfermedades_respiratorias']

        widgets = {
            'enfermedades_respiratorias': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'patologias': forms.CheckboxInput(attrs={'class': 'form-check-input'})}