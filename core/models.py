from django.db import models
import json
import requests
from cloudinary.models import CloudinaryField
from django import forms
from captcha.fields import CaptchaField

# Create your models here.
class TipoCliente(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Cliente(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, default='Apellido Default')
    edad = models.IntegerField(default=0)
    direccion = models.CharField(max_length=60, default='direccion Default')
    telefono = models.CharField(max_length=12)
    Premium = models.BooleanField(default=True)
    genero = models.CharField(max_length=10, choices=[('masculino','Masculino'),('femenino','Femenino')])
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    tipo = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)
    imagen = CloudinaryField('image')

    def __str__(self):
        return self.rut

    
class Categoria(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Noticia(models.Model):
    idNoticia = models.CharField(max_length=12)
    titulo_noticia = models.CharField(max_length=100)
    Autor = models.CharField(max_length=40)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    resumen = models.CharField(max_length=400)
    encabezado=models.CharField(max_length=300)
    cuerpo=models.CharField(max_length=3000)
    imagen= models.ImageField(upload_to="Noticia", blank=True, null=True)
    Categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.idNoticia