from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
import random



# Create your views here.
def index(request):
    return render(request,'index.html')

def registrarse(request):
    form=UsuarioRegistroForm()
    if request.method=='POST':
        form=UsuarioRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form=UsuarioRegistroForm()           
    return render(request,'registrarse.html',{'form':form})

@login_required(login_url='login')
def perfil(request):
    return render(request,'perfil.html')

@login_required(login_url='login')
def perfil_admin(request):
    return render(request,'perfilAdmin.html')



        




def login_usuario(request):
    user_message=request.GET.get('message',None)  
    
    if request.method=="POST":
        form=UsuarioLoginForm(data=request.POST)
        
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    return redirect('perfiladmin')
                else:
                    return redirect('perfil')
            else:
                user_message="Usuario o contraseña incorrectos."
        else:
            user_message="Por favor, ingrese un usuario y contraseña válidos."
            
    else:
        form=UsuarioLoginForm()
        
    return render(request,'login.html',{'form':form,'user_message':user_message})

def cerrar_sesion(request):
    logout(request)
    return redirect(reverse('login')+"?message=Has cerrado sesión correctamente.")



#crear post
def publicacion(request):
    current_usuario = get_object_or_404(Usuario, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            posteo = form.save(commit=False)
            posteo.usuario = current_usuario
            posteo.save()
            return redirect('publicacion')
    else:
        form = PostForm()
    publicaciones = Post.objects.all()
    comentarios = Comentario.objects.all()  # Obtener todos los comentarios
    form_comentario = ComentarioForm()  # Formulario para agregar comentarios
    return render(request, 'foro.html', {'form': form, 'publicaciones': publicaciones, 'comentarios': comentarios, 'form_comentario': form_comentario})


#crear comentario
def comentar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Post, id=publicacion_id)
    form_comentario = ComentarioForm(request.POST)
    if form_comentario.is_valid():
        comentario = form_comentario.save(commit=False)
        comentario.usuario = request.user
        comentario.post = publicacion
        comentario.save()
        return redirect('publicacion')
    else:
        form_comentario = ComentarioForm()
        pass



@login_required
def eliminar_publicacion(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.usuario == request.user:
        post.delete()
    return redirect('publicacion')


@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.usuario == request.user:
        comentario.delete()
    return redirect('publicacion')
