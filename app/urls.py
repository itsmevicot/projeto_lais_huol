from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = 'login'),
    path('usuario/cadastro', views.cadastro, name='cadastro'),
    path('home', views.home, name ='home'),
    path('logout', views.logout_user, name = 'logout'),
    path('buscar_agendamentos', views.buscar_agendamentos, name ='buscar_agendamentos'),
    path('listagem', views.listagem_agendamentos, name ='listagem'),
    path('realizar_agendamento/<int:id_agendamento>/', views.realizar_agendamento, name='realizar_agendamento'),

]