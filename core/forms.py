from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1","password2"]
    
class ClienteForm (ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class NoticiasForm (ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'

class TipoClienteForm (ModelForm):
    class Meta:
        model = TipoCliente
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']



