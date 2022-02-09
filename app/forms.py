from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column, Row
from django import forms
from django.utils.datetime_safe import date
from localflavor.br.forms import BRCPFField

from app.models import CustomUser
from lais_huol import settings
from dateutil.relativedelta import relativedelta


class cadastroForm(forms.Form):
    nome_completo = forms.CharField(label = 'Nome Completo', max_length=100)
    cpf = BRCPFField(label = 'CPF', max_length=11,widget = forms.TextInput(attrs={'data-mask':"00000000000"}))
    data_nascimento = forms.DateField(label = 'Data de Nascimento',widget = forms.TextInput(attrs={'data-mask':"00/00/0000"}))
    senha = forms.CharField(label = 'Senha', max_length=16, min_length= 8, widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(label = 'Confirmação de Senha', max_length=16, min_length=8, widget=forms.PasswordInput())


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
            Submit('submit', 'Submit', css_class='btn-primary'))

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

    def get_idade(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        idade = relativedelta(date.today(), data_nascimento).years
        return idade



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
            Submit('submit', 'Submit', css_class='btn-primary'))

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
