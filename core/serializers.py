from rest_framework import serializers
from .models import *


#LO UTILIZAMOS PARA TRANSFORMAR PYTHON A JSON
class TipoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCliente
        fields = '__all__' 

class ClienteSerializer(serializers.ModelSerializer):
    tipo = TipoClienteSerializer(read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__' 

class NoticiaSerializer(serializers.ModelSerializer):
    tipo = TipoClienteSerializer(read_only=True)
    
    class Meta:
        model = Noticia
        fields = '__all__' 