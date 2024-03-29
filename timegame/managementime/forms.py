#Importes de django
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import *
#Otros modulos
from datetime import datetime
from .models import *

class GameTimeForm(forms.ModelForm):
    end_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'step': 60, 'format': '%H:%M', 'class':'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}))
    
    class Meta:
        model = GameTime
        fields = ['console', 'hours', 'minutes','end_time','extra_controller', 'is_completed','is_active']
        required = {
            'hours': True,
            'minutes': True,
            'end_time': False,
        }
        widgets = {
            'console': forms.Select(attrs={'class': 'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline'}),
            'hours': forms.NumberInput(attrs={'class':'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-amber-400', 'placeholder':'Horas', 'value':'0'}),
            'minutes': forms.NumberInput(attrs={'class':'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Minutos', 'value':'0'}),
            'extra_controller': forms.NumberInput(attrs={'class':'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Cantidad de controles extra'}),
            'is_completed': CheckboxInput(attrs={'class':'form-checkbox text-indigo-600 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'is_active': CheckboxInput(attrs={'class':'form-checkbox text-indigo-600 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('hours')
        minutes = cleaned_data.get('minutes')
        extra_controller = cleaned_data.get('extra_controller')
        
        if hours < 0 or minutes < 0 or minutes > 60:
            raise forms.ValidationError('El valor de horas o minutos es inválido.')
        
        if extra_controller > 3 or extra_controller < 0:
            raise forms.ValidationError('El número de controles extra no puede ser mayor a 3 ni menor a 0')

        while minutes >= 60:
            hours += 1
            minutes -= 60
        cleaned_data['hours'] = hours
        cleaned_data['minutes'] = minutes
        return cleaned_data

class ConsoleForm(forms.ModelForm):
    class Meta:
        model = Console
        fields = '__all__'
        widgets= {
            'name': forms.TextInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Nombre'})
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name.capitalize()

class ReportForm(forms.Form):

    start_date = forms.DateField(
        label='Fecha inicial',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
    )

    end_date = forms.DateField(
        label='Fecha final',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
    )
    console = forms.ModelChoiceField(queryset=Console.objects.all(), required=False, widget=forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}))
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('La fecha inicial debe ser anterior a la fecha final.')

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.capitalize()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso.')

        return email
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 
                'placeholder':'Correo electronico'
            }))
    
    username = forms.CharField(
        label=("Nombre de usuario"),
        max_length=30,
        widget=forms.TextInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Nombre de usuario'}),
    )

    password1 = forms.CharField(
        label=("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Contraseña'}),
    )

    password2 = forms.CharField(
        label=("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Repetir contraseña'}),
        strip=False,
        help_text=("Ingresa la misma contraseña que antes, para verificarla."),
    )

class CustomUserChangeForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Nombre de usuario'
        })
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Correo electrónico'
        })
    )
    is_active = forms.BooleanField(
        label="Cuenta activa",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox text-indigo-600 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        }),
        required=False
    )
    is_staff = forms.BooleanField(
        label="Administrador",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox text-indigo-600 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        }),
        required=False
    )
    is_superuser = forms.BooleanField(
        label="Superusuario",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox text-indigo-600 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':' Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Contraseña'}))

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Correo electronico'
    }))

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Contraseña antigua'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Nueva contraseña'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Confirmar nueva contraseña'}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Contraseña nueva'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Repetir contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline', 'placeholder':'Contraseña nueva'}),
    )

class BackupForm(forms.Form):
    backup_file = forms.FileField(
        label='Seleccione el archivo de copia de seguridad',
        help_text='El archivo debe estar en formato JSON'
    )
    
    def clean_backup_file(self):
        backup_file = self.cleaned_data.get('backup_file')
        if backup_file:
            if not backup_file.name.endswith('.json'):
                raise forms.ValidationError('El archivo debe estar en formato JSON')
        return backup_file