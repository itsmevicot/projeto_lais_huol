from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from app.forms import cadastroForm, loginForm, agendamentoForm
from app.models import CustomUser, Agendamento_Cidadao, Agendamento
from django.contrib import auth, messages
from datetime import datetime


def cadastro(request):
    form = cadastroForm(request.POST or None)

    if request.method == 'POST':
        form = cadastroForm(request.POST)
        if form.is_valid():
            novo_usuario = CustomUser.objects.create_user(cpf = form.cleaned_data.get('cpf'), nome_completo= form.cleaned_data.get('nome_completo'),
                                                          data_nascimento= form.cleaned_data.get('data_nascimento'), password= form.cleaned_data.get('senha'))
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('login')

    return render(request,'usuarios/cadastro.html', locals())

def login(request):
    form = loginForm(request.POST or None)

    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            print("formulario valido")
            user = auth.authenticate(username = form.cleaned_data.get('cpf'), password= form.cleaned_data.get('senha'))
            if user is not None:
                auth.login(request,user)
                return redirect(home)
    return render(request, 'usuarios/login.html',locals())


@login_required(login_url='/')
def home(request):
    return render(request, 'usuarios/home.html')


@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def buscar_agendamentos(request):

    if Agendamento_Cidadao.objects.filter(cidadao= request.user, is_active= True).exists():
        return redirect('listagem')

    form = agendamentoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            dados_estabelecimento = form.cleaned_data.get('estabelecimento_saude')
            data_agendamento = form.cleaned_data.get('data_agendamento')

            horarios_possiveis = (
                ("8:0", "08h:00m"),
                ("8:10", "08h:10m"),
                ("8:20", "08h:20m"),
                ("8:30", "08h:30m"),
                ("8:40", "08h:40m"),
                ("8:50", "08h:50m"),
                ("9:0", "09h:00m"),
                ("9:10", "09h:10m"),
                ("9:20", "09h:20m"),
                ("9:30", "09h:30m"),
                ("9:40", "09h:40m"),
                ("9:50", "09h:50m"),
                ("10:0", "10h:00m"),
                ("10:10", "10h:10m"),
                ("10:20", "10h:20m"),
                ("10:30", "10h:30m"),
                ("10:40", "10h:40m"),
                ("10:50", "10h:50m"),
                ("11:0", "11h:00m"),
                ("11:10", "11h:10m"),
                ("11:20", "11h:20m"),
                ("11:30", "11h:30m"),
                ("11:40", "11h:40m"),
                ("11:50", "11h:50m"),
            )

            agendamento = Agendamento.objects.filter(data_agendamento= data_agendamento, estabelecimento=dados_estabelecimento).first()

            if agendamento == None:
                messages.success(request, "Não há horários disponíveis para o dia escolhido. Por favor, escolha outra data.")
                return render(request, 'autenticado/agendamento.html', locals())

            agendamentos_cidadao = Agendamento_Cidadao.objects.filter(agendamento_id = agendamento.pk)

            horarios_ocupados = []
            for agendamento_cidadao in agendamentos_cidadao:
                hora = agendamento_cidadao.hora_agendamento.hour
                minuto = agendamento_cidadao.hora_agendamento.minute
                horarios_ocupados.append(f"{hora}:{minuto}")

            print("Horarios ocupados: ", horarios_ocupados)
            todos_horarios_disponiveis = [x for x in horarios_possiveis if x[0] not in horarios_ocupados]
            print("Horários disponíveis: ", todos_horarios_disponiveis)

        return render(request, 'autenticado/agendamento.html', locals())

    return render(request, 'autenticado/agendamento.html', locals())


@login_required(login_url='/')
def realizar_agendamento(request, id_agendamento):
    horario = request.GET.get('horario')
    agendamento = Agendamento.objects.get(id = id_agendamento)
    horario = datetime.strptime(horario, "%H:%M").time()
    print(horario)
    novo_agendamento = Agendamento_Cidadao.objects.create(agendamento = agendamento, cidadao= request.user, is_active= True, hora_agendamento= horario)

    messages.success(request, "Agendamento feito com sucesso!")
    return redirect('listagem')


@login_required(login_url='/')
def listagem_agendamentos(request):
    agendamentos = Agendamento_Cidadao.objects.filter(cidadao= request.user)
    return render(request, 'autenticado/listagem.html', locals())


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def grafico_pizza(request):
    queryset = Agendamento.objects.order_by('-estabelecimento_id')
    id_estabelecimento = queryset[0].estabelecimento.pk
    nome_estabelecimentos = [queryset[0].estabelecimento.nome_estabelecimento]
    qtdade_agendamentos = []
    count = 0

    for agendamento in queryset:
        if id_estabelecimento == agendamento.estabelecimento.pk:
            count += 1

        else:
            id_estabelecimento = agendamento.estabelecimento.pk
            qtdade_agendamentos.append(count)
            count = 0
            nome_estabelecimentos.append(agendamento.estabelecimento.nome_estabelecimento)

    return render(request, 'graficos/grafico_pizza.html', locals())

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def grafico_barra(request):
    queryset = Agendamento_Cidadao.objects.order_by('-agendamento__estabelecimento_id')
    id_estabelecimento = queryset[0].agendamento.estabelecimento.pk
    nome_estabelecimentos = [queryset[0].agendamento.estabelecimento.nome_estabelecimento]
    qtdade_agendamentos = []
    count = 0

    for agendamento in queryset:
        if id_estabelecimento == agendamento.agendamento.estabelecimento.pk:
            count += 1

        else:
            qtdade_agendamentos.append(count)
            id_estabelecimento = agendamento.agendamento.estabelecimento.pk
            count = 1
            nome_estabelecimentos.append(agendamento.agendamento.estabelecimento.nome_estabelecimento)

    qtdade_agendamentos.append(count)

    return render(request, 'graficos/grafico_barra.html', locals())