from django.urls import path, include
from .views import *

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='inicio'),

    path('consultas/', consultas, name='consultas'),









#-------////----------BUSCAR PACIENTE--------////------------------# 

    path('buscar_paciente/', buscar_paciente, name='buscar_paciente'),

    path('buscar_paciente2/', buscar_paciente2, name='buscar_paciente2'),

#-------////----------FIN BUSCAR PACIENTE--------////------------------# 


    path('aboutme/', aboutme, name='aboutme'),







#-------////----------CREATE BASE VIEW HISTORIA CLINICA--------////------------------# 

path('perfilpaciente_list.html', PacienteList.as_view() , name='lista_pacientes'),

path('delete_pacientes.html/<int:pk>/', PacienteDelete.as_view() , name='delete_pacientes'),

path('detail_historia/<int:pk>/', PacienteDetail.as_view(), name="detail_historia"),


path('update_historia/<int:pk>/', HistoriaClinicaUpdate.as_view(), name='update_historia'),

#-------////----------FIN CREATE BASE VIEW HISTORIA CLINICA--------////------------------# 









#---------////--------------LOG IN---------////----------------------# 

    path('login/', login_request, name='login'),









#---------////--------------LOG OUT--------////----------------------# 

    path('logout/', LogoutView.as_view(template_name="aplicacion/index.html"), name='logout'),










#---------////--------------Turnos---------////----------------------#

    path('turnos/', turnos , name='turnos'),   


#---------////--------------FINTurnos---------////----------------------#









#---------////--------------REGISTRAR USUARIO--------////------------# 

    path('register/', register, name="register"),
    path('registeradmin/', registeradmin, name="registeradmin"),







#---------////--------------EDITAR USUARIO Y AVATAR---------////--------------#    

    path('editarusuario/', editarUsuario, name="editarusuario"),

]

