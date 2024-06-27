from django.shortcuts import render, redirect, get_object_or_404
from core.models import *
from core.forms import *
from core.models import Cliente 
from core.models import Noticia
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from rest_framework import viewsets
from core.serializers import *
import os
from rest_framework.renderers import JSONRenderer
import requests 
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt  # Importa si no lo tienes
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.conf import settings

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.conf import settings

def generar_voucher_pdf(request):
    # Información del pago (ejemplo)
    nombre_cliente = "Vicente Sepulveda"
    cantidad_pago = 5.99
    producto_comprado = "CaosNews x Spotify Premium"

    # Creación del documento PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="voucher.pdf"'

    # Crear el canvas para el PDF
    p = canvas.Canvas(response, pagesize=letter)

    # Agregar logo del noticiero
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'core', 'assets', 'img', 'logo', 'logo2.png')
    logo_height = 150  # Altura del logo
    logo_width = 300  # Ancho del logo
    x_logo = (letter[0] - logo_width) / 2  # Centrar el logo horizontalmente
    y_logo = letter[1] - 250  # Colocar el logo más abajo
    if os.path.exists(logo_path):
        p.drawImage(logo_path, x_logo, y_logo, width=logo_width, height=logo_height)

    # Título del voucher
    p.setFont("Helvetica-Bold", 20)
    title_text = "Voucher de Pago"
    title_width = p.stringWidth(title_text, "Helvetica-Bold", 20)
    p.drawCentredString(letter[0] / 2, y_logo - 100, title_text)

    # Detalles del cliente y producto
    p.setFont("Helvetica", 12)
    y_details = y_logo - 200  # Colocar detalles más abajo
    p.drawString(letter[0] / 2 - title_width / 2, y_details, f"Cliente: {nombre_cliente}")
    p.drawString(letter[0] / 2 - title_width / 2, y_details - 20, f"Producto: {producto_comprado}")
    p.drawString(letter[0] / 2 - title_width / 2, y_details - 40, f"Cantidad: ${cantidad_pago}")

    # Línea divisoria
    p.line(letter[0] / 2 - title_width / 2, y_details - 60, letter[0] / 2 + title_width / 2, y_details - 60)

    # Otros detalles y estilos pueden ser agregados según tu necesidad

    p.showPage()
    p.save()

    return response

#API

def clienteapi(request):
    response = requests.get('http://127.0.0.1:8000/api/clientes/')
    response2 = requests.get('https://randomuser.me/api/?results=100')  # Cambio a la API de usuarios random
    cliente = response.json()
    usuarios_random = response2.json()['results']  # Obtener resultados de usuarios random

    paginator = Paginator(usuarios_random, 10)  # Muestra 10 usuarios por página
    page_number = request.GET.get('page')  # Busca el número de página
    page_obj = paginator.get_page(page_number)

    aux = {
        'lista': cliente,
        'page_obj': page_obj 
    }

    return render(request, 'core/crudapi/index3.html', aux)

# UTILIZAMOS LOS VIEWSET PARA MANEJAR LAS SOLICITUDES HTTP (GET, POST, PUT, DELETE)
class TipoClienteViewset (viewsets.ModelViewSet):
    queryset = TipoCliente.objects.all()
    serializer_class = TipoClienteSerializer
    renderer_classes = [JSONRenderer]

class ClienteViewset (viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    renderer_classes = [JSONRenderer]   

class NoticiaViewset (viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer
    renderer_classes = [JSONRenderer]

def noticiadetalle(request, id):
    try:
        response = requests.get(f'http://127.0.0.1:8000/api/noticias/{id}/')
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado 4xx/5xx

        try:
            noticia = response.json()
        except ValueError:
            return render(request, 'core/crudapi/error.html', {'error': 'Invalid JSON response from API'})

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return render(request, 'core/crudapi/error.html', {'error': 'Noticia no encontrada'})
        else:
            return render(request, 'core/crudapi/error.html', {'error': f'Error de solicitud: {str(e)}'})

    except requests.exceptions.RequestException as e:
        return render(request, 'core/crudapi/error.html', {'error': str(e)})

    context = {
        'noticia': noticia,
    }

    return render(request, 'core/crudapi/detalle.html', context)

# Create your views here.
def user_in_group(user, group_name):
    # Esta función debe verificar si el usuario pertenece al grupo especificado.
    # Implementación depende de tu modelo de usuario y grupos.
    return user.groups.filter(name=group_name).exists()

def group_required(group_name):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if user_in_group(request.user, group_name):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator

def index(request):
    noticias = Noticia.objects.all()
    noticiaM = Noticia.objects.get(idNoticia='1')
    noticiaM = Noticia.objects.get(idNoticia='2')
    return render(request, 'core/index.html', {'noticias': noticias,'noticia1': noticiaM})


def register (request):
    return render(request, 'registration/register.html')


def about(request):
    return render(request, 'core/about.html')

def categori(request):
    return render(request, 'core/Paginas/categori.html')


def latest_news(request):
    noticias_list = Noticia.objects.all()  
    context = {
        'noticias': noticias_list
    }
    return render(request, 'core/Paginas/latest_news.html', context)

def blog(request):
    return render(request, 'core/Paginas/blog.html')

def blog_details(request):
    return render(request, 'core/Paginas/blog_details.html')

def elements(request):
    return render(request, 'core/Paginas/elements.html')

def contact(request):
    return render(request, 'core/Paginas/contact.html')

def noticias(request):
    return render(request, 'core/empleados/crud/add.html')


def basededatos (request):
    return render (request, 'core/Clientes/crud/basededatos.html')

def spotify (request):
    return render (request, 'core/Paginas/spotify.html')


def detalle_noticia(request, id_noticia):
    noticia = Noticia.objects.get(idNoticia=id_noticia)
    return render(request, 'core/Paginas/detalle_noticia.html', {'noticia': noticia})


def homepage_view(request):
    aux = {
        "users_count": Cliente.objects.count()
    }
    return render(request, 'core/Clientes/principal.html', aux)


def cliente (request):
    cliente = Cliente.objects.all()
    aux = {
        'lista' : cliente
    }

    return render(request, 'core/Clientes/index2.html', aux)

@group_required('cliente')
def noticias(request):
    noticias_list = Noticia.objects.all()  # Obtener todas las noticias
    aux = {
        'noticias': noticias_list  # Pasar la lista de noticias al contexto
    }

    return render(request, 'core/Clientes/ListarNoticia.html', aux)

@login_required
def principal(request):
    total_users = 10  # Ejemplo de total de usuarios
    total_noticias = 20  # Ejemplo de total de noticias
    total_reporteros = 5  # Ejemplo de total de reporteros
    total_supervisor = 2  # Ejemplo de total de supervisores
    
    context = {
        'total_users': total_users,
        'total_reporteros': total_reporteros,
        'total_supervisor': total_supervisor,
        'total_noticias': total_noticias,
    }
    
    return render(request, 'core/Clientes/principal.html', context)

@group_required('reportero')
def addnoticia(request):
    if request.method == 'POST':
        formulario = NoticiasForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            noticia = formulario.save()  # Guardar la noticia y obtener el objeto de noticia creado
            messages.success(request, "Noticia creada correctamente")
            # Redirigir al usuario a la página de noticias
            return redirect('latest_news')  # Redirige a la vista que muestra las últimas noticias
        else:
            messages.error(request, "Error al crear la noticia")
    
    aux = {
        'form': NoticiasForm(),
        'msj': ''  # Inicializa la variable 'msj' con un valor vacío
    }
    return render(request, 'core/Clientes/crud/addnoticia.html', aux)

@group_required('reportero')
def noticiasupdate(request, id):
    noticia = Noticia.objects.get(id=id)  # Cambio realizado aquí
    aux = {
        'form': NoticiasForm(instance=noticia)
    }
    
    if request.method == 'POST':
        formulario = NoticiasForm(data=request.POST, instance=noticia, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            messages.success(request, "Noticia actualizada correctamente")
        else:
            aux['form'] = formulario
            messages.error(request, "Error al actualizar la noticia")

    return render(request, 'core/Clientes/crud/updateNoticias.html', aux)

@group_required('reportero')
def noticiasdelete(request, id):
    noticia = Noticia.objects.get(id=id) 
    noticia.delete()
    return redirect('noticias')



def clientesadd(request):
    aux = {
        'form': ClienteForm(),
        'msj': ''  # Inicializa la variable 'msj' con un valor vacío
    }

    if request.method == 'POST':
        formulario = ClienteForm(request.POST, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Usuario creado correctamente")
        else:
            aux['form'] = formulario
            messages.error(request,"Error al crear el Usuario")
    return render(request, 'core/Clientes/crud/add.html', aux)


@permission_required('core.change_cliente')
def clientesupdate(request, id):
    cliente = Cliente.objects.get(id = id) 
    aux = {
        'form' : ClienteForm(instance=cliente)
    }
    
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, instance=cliente, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux ['form'] = formulario
            messages.success(request,"Usuario actualizado correctamente")
        else:
            aux ['form'] = formulario
            messages.error(request,"Error al actualizar el usuario")

    return render(request, 'core/Clientes/crud/update.html', aux)


@permission_required('core.delete_cliente')
def clientesdelete (request, id):

    cliente = Cliente.objects.get(id = id) 
    cliente.delete()
    
    return redirect(to="cliente")


def register (request):

    aux = {
        'form' : CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            group = Group.objects.get(name='Cliente')
            user.groups.add(group)

            messages.success(request,"Usuario creado correctamente")
            return redirect(to="index")
        else:
            aux['form'] = formulario
    return render(request, 'registration/register.html', aux)


def account_locked(request):
    return render(request, 'core/account_locked.html')
