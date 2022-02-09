from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('usuario/cadastro', views.cadastro, name='cadastro'),
    path('usuario/login', views.login, name='login'),
    path('home', views.home, name ='home'),
    path('logout', views.logout_user, name = 'logout'),
    path('agendamento', views.agendamento, name ='agendamento'),
    path('listagem', views.listagem_agendamentos, name ='listagem')

]