from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.forms import cadastroForm, loginForm
from app.models import CustomUser
from django.contrib import auth, messages


def index(request):
    return render(request,'index.html')

def cadastro(request):
    form = cadastroForm(request.POST or None)

    if request.method == 'POST':
        form = cadastroForm(request.POST)
        if form.is_valid():
            novo_usuario = CustomUser.objects.create_user(cpf = form.cleaned_data.get('cpf'), nome_completo= form.cleaned_data.get('nome_completo'),
                                                          data_nascimento= form.cleaned_data.get('data_nascimento'), password= form.cleaned_data.get('senha'))
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('index')

    return render(request, 'usuarios/cadastro.html', locals())

def login(request):
    form = loginForm(request.POST or None)

    if request.method == 'POST':
        form = loginForm(request.POST)
        print("NÃO ENTROU NO É VÁLIDO")
        if form.is_valid():
            print("É VÁLIDO")
            print(f"CPF: {form.cleaned_data['cpf']}, Senha: {form.cleaned_data['senha']}")
            user = auth.authenticate(username = form.cleaned_data.get('cpf'), password= form.cleaned_data.get('senha'))
            print(user)
            if user is not None:
                print("teste:", user)
                auth.login(request,user)
                return redirect(home)
    return render(request, 'usuarios/login.html',locals())

@login_required(login_url='/usuario/login/')
def logout_user(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/usuario/login')
def home(request):
    return render(request, 'usuarios/home.html')

@login_required(login_url='/usuario/login')
def agendamento(request):
    return render(request, 'autenticado/agendamento.html')

@login_required(login_url='/usuario/login')
def listagem_agendamentos(request):
    return render(request, 'autenticado/listagem.html')