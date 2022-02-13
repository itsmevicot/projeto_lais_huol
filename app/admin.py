from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from app.models import CustomUser, Estabelecimento, Agendamento_Cidadao, Agendamento


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('cpf','data_nascimento','nome_completo')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não conferem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('nome_completo','data_nascimento','is_active', 'is_admin', 'is_staff', 'is_superuser')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('nome_completo','cpf','data_nascimento','is_active', 'is_admin', 'is_staff', 'is_superuser',)
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Personal info', {'fields': ('nome_completo','data_nascimento',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome_completo','cpf','data_nascimento','password1','password2',)
        }),
    )

    search_fields = ('cpf',)
    ordering = ('cpf',)
    filter_horizontal = ()

@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_filter= ('nome_estabelecimento', 'codigo_cnes',)
    list_display= ('nome_estabelecimento', 'codigo_cnes',)
    search_fields= ('nome_estabelecimento', 'codigo_cnes',)
    ordering= ('nome_estabelecimento', 'codigo_cnes',)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_filter= ('estabelecimento', 'data_agendamento',)
    list_display= ('estabelecimento', 'data_agendamento',)
    search_fields= ('estabelecimento', 'data_agendamento',)
    ordering= ('estabelecimento', 'data_agendamento',)


@admin.register(Agendamento_Cidadao)
class Agendamento_CidadaoAdmin(admin.ModelAdmin):
    list_filter= ('agendamento', 'cidadao','hora_agendamento', 'is_active',)
    list_display= ('agendamento', 'cidadao','hora_agendamento', 'is_active',)
    search_fields= ('agendamento', 'cidadao','hora_agendamento', 'is_active',)
    ordering= ('agendamento', 'cidadao','hora_agendamento', 'is_active',)


admin.site.register(CustomUser, UserAdmin)

