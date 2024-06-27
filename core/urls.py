from django.urls import path, include
from .views import *
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

#CONFIGURACION DEL APPI
router = routers.DefaultRouter()

# Registra los viewsets con el router
router.register('tipoclientes', TipoClienteViewset)
router.register('clientes', ClienteViewset)
router.register('noticias', NoticiaViewset)



urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cliente/', cliente, name="cliente"),
    path('noticias/', noticias, name="noticias"),
    path('basededatos/', basededatos, name="basededatos"),
    path('clientesadd/', clientesadd, name="clientesadd"),
    path('clientes/update/<id>', clientesupdate, name="clientesupdate"),    
    path('clientes/delete/<id>', clientesdelete, name="clientesdelete"),
    path('categori/', categori, name='categori'),
    path('latest_news/', latest_news, name="latest_news"),
    path('blog/', blog, name="blog"),
    path('blog_details/', blog_details, name="blog_details"),
    path('elements/', elements, name="elements"),
    path('contact/', contact, name="contact"),
    path('addnoticia/', addnoticia, name="addnoticia"),
    path('noticias/update/<id>', noticiasupdate, name="noticiasupdate"),    
    path('noticias/delete/<id>', noticiasdelete, name="noticiasdelete"),
    path('detalle_noticia/<str:id_noticia>/', views.detalle_noticia, name="detalle_noticia"),
    path('principal/', principal, name="principal"),
    path('lockout/', account_locked, name='lockout'),
    path('spotify/', spotify, name='spotify'),
    path('generar-voucher/', views.generar_voucher_pdf, name='generar_voucher_pdf'),

    #API
    path('api/', include(router.urls) ),
    path('clienteapi/', clienteapi, name="clienteapi"),
    path('noticiadetalle/<id>/', noticiadetalle, name="noticiadetalle"),

    #REGISTER
    path('register', register, name="register"),
    
]