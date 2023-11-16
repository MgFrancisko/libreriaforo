"""
URL configuration for LibreriaFPV project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from libreriaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfiladmin/', views.perfil_admin, name='perfiladmin'),
    path('foro/', views.publicacion, name='publicacion'),
   
    path('foro/<int:publicacion_id>/', views.comentar_publicacion, name='comentar_publicacion'),
    
    path('eliminar_publicacion/<int:post_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),



]
