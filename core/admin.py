from django.contrib import admin
from .models import *
from admin_confirm import AdminConfirmMixin

class TipoClienteAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['descripcion']

class ClienteAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['rut', 'nombre', 'apellido', 'email', 'telefono']

# Register your models here.
admin.site.register(TipoCliente, TipoClienteAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Noticia)
admin.site.register(Categoria)

