from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column, Row
from django import forms
from django.utils.datetime_safe import date
from localflavor.br.forms import BRCPFField
from app.models import CustomUser, Estabelecimento
from dateutil.relativedelta import relativedelta
from bootstrap_datepicker_plus.widgets import DatePickerInput


class cadastroForm(forms.Form):
    nome_completo = forms.CharField(label= 'Nome Completo', max_length=100)
    cpf = BRCPFField(label= 'CPF', max_length=11,widget= forms.TextInput(attrs={'data-mask':"00000000000"}))
    data_nascimento = forms.DateField(label= 'Data de Nascimento',widget= forms.TextInput(attrs={'data-mask':"00/00/0000"}))
    senha = forms.CharField(label= 'Senha', max_length=16, min_length= 8, widget= forms.PasswordInput())
    confirmar_senha = forms.CharField(label = 'Confirmação de Senha', max_length=16, min_length=8, widget= forms.PasswordInput())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("nome_completo",css_class="form-group col-12 col-md-10"),
                Column("cpf", css_class="form-group col-12 col-md-10"),
                Column("data_nascimento", css_class="form-group col-12 col-md-10"),
                Column("senha", css_class="form-group col-12 col-md-10"),
                Column("confirmar_senha", css_class="form-group col-12 col-md-10"),
            ),
            Submit('submit', 'Cadastrar', css_class='btn-primary'))

    def clean_nome_completo(self):
        nome_completo = self.cleaned_data.get('nome_completo')
        if any(char.isdigit() for char in nome_completo):
            raise forms.ValidationError('O nome não pode conter dígitos.')
        return nome_completo

    def clean_confirmar_senha(self):
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não são iguais.")
        return confirmar_senha

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        idade = relativedelta(date.today(),data_nascimento).years
        if idade < 18:
            raise forms.ValidationError("Você precisa ser maior de 18 anos para se cadastrar no sistema.")
        return data_nascimento

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if CustomUser.objects.filter(cpf = cpf).exists():
            raise forms.ValidationError("O CPF inserido já é cadastrado.")
        return cpf

class loginForm(forms.Form):
    cpf = BRCPFField(label='CPF', max_length=11, widget=forms.TextInput(attrs={'data-mask': "00000000000"}))
    senha = forms.CharField(label='Senha', max_length=16, min_length=8, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("cpf", css_class="form-group col-12 col-md-10"),
                Column("senha", css_class="form-group col-12 col-md-10"),
            ),
            Submit('submit', 'Acessar o sistema', css_class='btn-primary'))

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf == "":
            raise forms.ValidationError("O campo CPF deve ser preenchido.")
        if not CustomUser.objects.filter(cpf = cpf).exists():
            raise forms.ValidationError("Esse CPF não está cadastrado.")
        return cpf

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if senha == "":
            raise forms.ValidationError("O campo Senha deve ser preenchido.")
        return senha

class agendamentoForm(forms.Form):
    estabelecimento_saude = forms.ModelChoiceField(queryset=Estabelecimento.objects.all(), label="Estabelecimento de Saúde")
    data_agendamento = forms.DateField(label='Data do Exame', widget=DatePickerInput(format='%d/%m/%Y', options={"locale":"pt_br"}))

    horarios_possiveis = (
        ("8:0", "08h:00m ~ 08h:10m"),
        ("8:10", "08h:10m ~ 08h:20m"),
        ("8:20", "08h:20m ~ 08h:30m"),
        ("8:30", "08h:30m ~ 08h:40m"),
        ("8:40", "08h:40m ~ 08h:50m"),
        ("8:50", "08h:50m ~ 09h:00m"),
        ("9:0",  "09h:00m ~ 09h:10m"),
        ("9:10", "09h:10m ~ 09h:20m"),
        ("9:20", "09h:20m ~ 09h:30m"),
        ("9:30", "09h:30m ~ 09h:40m"),
        ("9:40", "09h:40m ~ 09h:50m"),
        ("9:50", "09h:50m ~ 10h:00m"),
        ("10:0", "10h:00m ~ 10h:10m"),
        ("10:10", "10h:10m ~ 10h:20m"),
        ("10:20", "10h:20m ~ 10h:30m"),
        ("10:30", "10h:30m ~ 10h:40m"),
        ("10:40", "10h:40m ~ 10h:50m"),
        ("10:50", "10h:50m ~ 11h:00m"),
        ("11:0", "11h:00m ~ 11h:10m"),
        ("11:10", "11h:10m ~ 11h:20m"),
        ("11:20", "11h:20m ~ 11h:30m"),
        ("11:30", "11h:30m ~ 11h:40m"),
        ("11:40", "11h:40m ~ 11h:50m"),
        ("11:50", "11h:50m ~ 12h:00m"),
    )
    #hora_agendamento = forms.ChoiceField(label='Hora do Exame', choices=horarios_possiveis, widget=forms.Select)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("estabelecimento_saude", css_class="form-group col-12 col-md-10"),
                Column("data_agendamento",css_class="form-group col-12 col-md-10"),
            ),
            Submit('submit', 'Buscar horários disponíveis', css_class='btn-primary'))


    def clean_data_agendamento(self):
        data_agendamento = self.cleaned_data.get('data_agendamento')
        data_agora = date.today()
        if data_agendamento < data_agora:
            raise forms.ValidationError("Não é possível marcar um exame para uma data já passada.")
        if data_agendamento.weekday() == 5 or data_agendamento.weekday() == 6:
            raise forms.ValidationError("Não é possível marcar exames no final de semana.")
        return data_agendamento