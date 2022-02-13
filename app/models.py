from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.timezone import localtime
from localflavor.br.models import BRCPFField


class CustomUserManager(BaseUserManager):

    def create_user(self, cpf, nome_completo, data_nascimento, password = None): #precisa passar o isActive ???

        if not cpf:
            raise ValueError(('O campo CPF é obrigatório.'))

        user = self.model(
            nome_completo = nome_completo,
            data_nascimento = data_nascimento,
            cpf = cpf
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, cpf, nome_completo, data_nascimento, password = None):

        user = self.create_user(
            nome_completo = nome_completo,
            data_nascimento=data_nascimento,
            cpf=cpf,
            password= password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    cpf = BRCPFField(
        max_length = 11,
        unique = True,
        verbose_name = ('CPF'),
        help_text = ('Esse campo é obrigatório. Máximo de 11 dígitos.'),
        error_messages = {
            'unique': ("Esse CPF já é cadastrado no sistema."),
        },
    )

    nome_completo = models.CharField(('nome completo'), max_length=150, blank=False)
    data_nascimento = models.DateField(('data de nascimento'))
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_staff = models.BooleanField(default=False, verbose_name='Faz parte da Administração')
    is_admin = models.BooleanField(default =False, verbose_name=('Administrador'))
    is_superuser = models.BooleanField(default=False, verbose_name=('Superuser'))
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name=('Data de Ingresso'))


    objects = CustomUserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome_completo','data_nascimento']

    class Meta:
        verbose_name = ('usuário')
        verbose_name_plural = ('usuários')

    def get_nome_completo(self):
        return self.nome_completo

    def get_cpf(self):
        return self.cpf

    def get_data_nascimento(self):
        return self.data_nascimento

    def get_idade(self):
        data_nascimento = self.data_nascimento
        idade = relativedelta(date.today(), data_nascimento).years
        return idade

    def get_primeiro_nome(self):
        return self.nome_completo.split()[0]


class Estabelecimento(models.Model):
    nome_estabelecimento = models.CharField('Nome do Estabelecimento', max_length=70)
    codigo_cnes = models.CharField('Código CNES', max_length=30)

    def __str__(self):
        return f"{self.nome_estabelecimento}, CNES: {self.codigo_cnes}"


class Agendamento(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, verbose_name="Estabelecimento")
    data_agendamento = models.DateField('Data do Agendamento')


class Agendamento_Cidadao(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, verbose_name="ID do Agendamento")
    cidadao = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="CPF")
    is_active = models.BooleanField(default=False, verbose_name='Agendamento Ativo')
    hora_agendamento = models.TimeField('Hora do Agendamento')


    @property
    def status_agendamento(self):
        if date.today() > self.agendamento.data_agendamento:
            return 'Expirado'
        elif date.today() == self.agendamento.data_agendamento:
            if localtime().time() < self.hora_agendamento:
                return 'Expirado'
        else:
            return 'Ativo'

        return 'Ativo'

    @property
    def datahora_consulta(self):
        return f"Sistema acessado às {localtime().time().strftime('%H:%M:%S')} no dia {date.today().strftime('%d/%m/%Y')}"

    @property
    def dia_semana(self):

        dias_semana = {0: 'Segunda-Feira',
                       1: 'Terça-Feira',
                       2: 'Quarta-Feira',
                       3: 'Quinta-Feira',
                       4: 'Sexta-Feira',
                       5: 'Sábado',
                       6: 'Domingo'}

        dia_agendamento = dias_semana[self.agendamento.data_agendamento.weekday()]
        return dia_agendamento