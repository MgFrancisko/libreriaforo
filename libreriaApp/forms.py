"""Aqui van los formularios que se renderizan en los templates a traves de las views, el uso del framework se encarga de las
validaciones de entrada de datos"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import *
from django.db import transaction

#Login
class UsuarioLoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de Usuario'}),label="")
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),label="")

#Creacion de un usuario
class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model=Usuario
        fields=('first_name','last_name','email','rut','username')
    
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),label="")    
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido'}),label="")  
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),label="")  
    rut=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'rut'}),label="")
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de Usuario'}),label="")
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),label="")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar Password'}),label="")
    
    #Esta funcion guarda el usuario y le asocia un perfil y un carro de compras unico
    def save(self,commit=True):
        """Aqui se usa una 'transacción atómica' para evitar inconsistencias en la base de datos
        en caso de que algo falle durante el proceso de guardado, asi si ocurre
        una excepcion los datos no se almacenan en la base de datos"""
        with transaction.atomic():
            usuario=super().save(commit=False)
            if commit:
                usuario.save()
                Perfil.objects.create(usuario=usuario)
                CarroDeCompra.objects.create(usuario=usuario)
        return usuario

#Modificar datos de usuario
User = get_user_model()
class CustomUserChangeForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=('first_name','last_name','email','rut','username')
    
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),label="")    
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido'}),label="")  
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),label="")  
    rut=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'rut'}),label="")
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de Usuario'}),label="")

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None) 

#Registra un Autor en el sistema
class AutorRegistroForm(forms.ModelForm):
    class Meta:
        model=Autor
        fields='__all__'

    nombreAutor=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Autor'}),label="")
    apellidoAutor=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Autor'}),label="")
    biografiaAutor=forms.CharField(max_length=5000,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Biografia'}),label="")

#Registra un Libro en el sistema 
class LibroRegistroForm(forms.ModelForm):
    class Meta:
        model=Libro
        fields='__all__'

    titulo=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),label="")
    autorlibro=forms.ModelChoiceField(queryset=Autor.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}),label="")
    tematica=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'tematica'}),label="")
    editorial=forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Editorial'}),label="")
    edicion=forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Edición'}),label="")
    fechaDePublicacion=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),label="")
    cantidad=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),label="")
    precio=forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),label="")
    disponible=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),label="",required=False)
    imagen=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}),label="",required=False)

    def clean_imagen(self):
        imagen=self.cleaned_data.get('imagen', False)
        if imagen:
            if imagen.size > 1 * 1024 * 1024:
                raise forms.ValidationError("El archivo de imagen es demasiado grande ( > 1mb ).")
            return imagen

    def save(self,commit=True):
        libro=super(LibroRegistroForm, self).save(commit=False)
        if self.cleaned_data.get('imagen'):
            imagen=self.cleaned_data['imagen']
            libro.imagen = imagen.read()
        if commit:
            libro.save()
        return libro

#Registra los datos del perfil de usuario
class PerfilRegistroForm(forms.ModelForm):
    class Meta:
        model=Perfil
        fields='__all__'
        exclude=('usuario',)
        
    biografiaPerfil=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Biografia'}),label='')
    areasDeInteres=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Areas de interes'}),label='')
    librosLeidos=forms.ModelMultipleChoiceField(queryset=Libro.objects.all(),widget=forms.CheckboxSelectMultiple(),label='')
    imagenPerfil=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}),label="",required=False)







class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('contenidoPost',)
    contenidoPost = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe un nuevo post', 'style': 'height:50px'}))
    

    

class ComentarioForm(forms.ModelForm):
     class Meta:
        model = Comentario
        fields = ('contenidoComentario',)
     contenidoComentario = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Agregar comentario', 'style' : 'height:20px'}))

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ('motivoReporte',)

    motivoReporte=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Explica tu reporte'})