from django.shortcuts import redirect, render
from .models import *
from .forms import *

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.views.generic import DeleteView


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import user_passes_test




#-------////----------INDEX--------////------------------# 

def index(request):
    return render (request, "aplicacion/index.html")

#-------////----------FIN INDEX--------////------------------# 

def aboutme(request):
    return render (request, "aplicacion/aboutme.html")






#-------////----------TURNOS--------////------------------# 

def turnos(request):
    return render (request, "aplicacion/turnos.html")

#-------////----------FIN TURNOS--------////------------------# 







#-------////----------FORM CONSULTAS--------////------------------# 
def consultas(request):
    if request.method == "POST":
        miformulario = ConsultasForm(request.POST)
        if miformulario.is_valid():
            informacion = miformulario.cleaned_data
            consulta = ConsultasModel(cnombre=informacion["cnombre"], capellido=informacion["capellido"], cemail=informacion["cemail"],cconsulta=informacion["cconsulta"])
            consulta.save()
            return render (request, "aplicacion/consultas.html", {"exito": True},)
    else:
        miformulario = ConsultasForm()

    return render (request, "aplicacion/consultas.html", {"form":miformulario})

#-------////----------FIN FORM CONSULTAS--------////------------------# 









#-------////----------SI ES ADMIN--------////------------------# 

def is_admin(user):
    return user.is_authenticated and user.is_superuser
#-------////----------FIN SI ES ADMIN--------////------------------# 








#-------////----------BUSCAR PACIENTE--------////------------------# 

@user_passes_test(is_admin)
def buscar_paciente(request):
    return render (request, "aplicacion/buscar_paciente.html")

@user_passes_test(is_admin)
def buscar_paciente2(request):
    if request.GET['first_name']:
        first_name = request.GET['first_name']
        paciente = Historia_ClinicaModel.objects.filter(perfil_paciente__nombre__iexact=first_name)
        return render(request, 
                      "aplicacion/listadopacientes.html", 
                      {"first_name": first_name, "paciente":paciente})
    return redirect ('lista_pacientes')


#-------////----------FIN BUSCAR PACIENTE--------////------------------# 








#-------////----------CREATE BASE VIEW HISTORIA CLINICA--------////------------------# 
class PacienteList(LoginRequiredMixin,ListView):
    model = PerfilPaciente
    context_object_name = 'paciente_list'

class PacienteDelete(LoginRequiredMixin, DeleteView):
    model = PerfilPaciente
    success_url = reverse_lazy('lista_pacientes') 

class HistoriaClinicaUpdate(LoginRequiredMixin,UpdateView):
    model = Historia_ClinicaModel
    # fields = ['perfil_paciente','patologias','enfermedades_respiratorias']
    form_class = HistoriaClinicaForm
    success_url = reverse_lazy('inicio')

class PacienteDetail(LoginRequiredMixin, DetailView):
    model = PerfilPaciente


#-------///////-----------FIN BASE VIWE HISTORIA CLINICA---------///////------------#











#------///////------------LOGIN-----------///////----------#

def login_request(request):
    if request.method == "POST":
        miForm = AuthenticationForm(request, data=request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            clave = miForm.cleaned_data.get('password')
            user = authenticate(username=usuario, password=clave)
            if user is not None:
                login(request, user)
                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = '/media/avatares/default.png'
                finally:
                    request.session['avatar'] = avatar
                    
                return render(request, "aplicacion/index.html", {"mensaje": f"Bienvenido {usuario}"})
            else:
                return render(request, "aplicacion/login.html", {"form":miForm, "mensaje": "Datos Inválidos"})
        else:    
            return render(request, "aplicacion/login.html", {"form":miForm, "mensaje": "Datos Inválidos"})

    miForm = AuthenticationForm()

    return render(request, "aplicacion/login.html", {"form":miForm})    



#-------///////-----------FIN LOGIN-------///////--------------#




#-------///////-----------ADMIN REGISTRA NUEVO PACIENTE---------///////------------#
@user_passes_test(is_admin)
def registeradmin(request):
    if request.method == 'POST':
        form = RegistroPacientesForm(request.POST) 
        if form.is_valid():
            user = form.save()  # Guarda el usuario y obtén la instancia

            # Crear un perfil de paciente relacionado y llenar algunos campos
            perfil = PerfilPaciente(usuario=user, nombre=user.first_name, apellido=user.last_name, email=user.email)
            perfil.save()

            historia_clinica = Historia_ClinicaModel(perfil_paciente=perfil)
            historia_clinica.save()
            
            return render(request, "aplicacion/index.html", {"mensaje": "Usuario Creado"})        
    else:
        form = RegistroPacientesForm()

    return render(request, "aplicacion/registroadmin.html", {"form": form}) 







#-------///////-----------REGISTRO---------///////------------#
def register(request):
    if request.method == 'POST':
        form = RegistroPacientesForm(request.POST) 
        if form.is_valid():
            user = form.save()  # Guarda el usuario y obtén la instancia

            # Crear un perfil de paciente relacionado y llenar algunos campos
            perfil = PerfilPaciente(usuario=user, nombre=user.first_name, apellido=user.last_name, email=user.email)
            perfil.save()

            historia_clinica = Historia_ClinicaModel(perfil_paciente=perfil)
            historia_clinica.save()

            # Iniciar sesión automáticamente al usuario
            login(request, user)
            
            return render(request, "aplicacion/index.html", {"mensaje": "Usuario Creado"})        
    else:
        form = RegistroPacientesForm()

    return render(request, "aplicacion/registro.html", {"form": form}) 

#------///////------------FIN REGISTRO--------///////-------------#









#------///////---------EDITAR PERFIL----------///////--------#


@login_required
def editarUsuario(request):
    usuario = request.user
    avatarViejo = Avatar.objects.filter(user=usuario)
    if request.method == "POST":
        form = EditarUsuario(request.POST)
        if form.is_valid():
            usuario.email = form.cleaned_data.get('email')
            usuario.password1 = form.cleaned_data.get('password1')
            usuario.password2 = form.cleaned_data.get('password2')
            usuario.first_name = form.cleaned_data.get('first_name')
            usuario.last_name = form.cleaned_data.get('last_name')
            usuario.save()

    # SI DESEA CAMBIAR EL AVATAR


            if request.FILES.get('imagen'):
                form = EditarUsuario(request.POST, request.FILES)
                if form.is_valid():
                    u = User.objects.get(username=request.user)
                    avatarViejo = Avatar.objects.filter(user=u)
                    if len(avatarViejo) > 0: 
                        avatarViejo[0].delete()
                    if form.cleaned_data['imagen']:
                        avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
                    avatar.save()
                    request.session['avatar'] = avatar.imagen.url
            return render(request, "aplicacion/index.html", {'mensaje': f"Usuario {usuario.username} actualizado correctamente"})
            
        else:
            return render(request, "aplicacion/editarusuario.html", {'form': form})
    else:
        form = EditarUsuario(instance=usuario)
    return render(request, "aplicacion/editarusuario.html", {'form': form, 'usuario':usuario.username})

#---------///////---------FIN EDITAR PERFIL-------///////--------------#
