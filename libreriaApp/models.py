"""El modelo es el que crea las tablas de la base de datos relacional donde se almacena la informacion
del sistema"""

from django.db import models
from django.contrib.auth.models import AbstractUser
  
# Create your models here.
class Usuario(AbstractUser):
    rut=models.CharField(max_length=10,unique=True)

class Autor(models.Model):
    nombreAutor=models.CharField(max_length=150)
    apellidoAutor=models.CharField(max_length=150)
    biografiaAutor=models.TextField(max_length=2500,blank=True)

class Libro(models.Model):
    titulo=models.CharField(max_length=200)
    imagen=models.ImageField(upload_to='imagenes_libros/',null=True,blank=True,editable=True)
    autorlibro=models.ForeignKey(Autor,on_delete=models.CASCADE)
    tematica=models.CharField(max_length=150)
    editorial=models.CharField(max_length=150)
    edicion=models.CharField(max_length=150)
    fechaDePublicacion=models.DateField()
    cantidad=models.IntegerField()
    precio=models.DecimalField(max_digits=5,decimal_places=2)
    disponible=models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

class CarroDeCompra(models.Model):
    usuario=models.OneToOneField(Usuario,on_delete=models.CASCADE)
    librosAcomprar=models.ManyToManyField(Libro,through='ItemCarro',blank=True)
    totalPrecio=models.DecimalField(max_digits=6,decimal_places=2,default=0.00)

class ItemCarro(models.Model):
    carro=models.ForeignKey(CarroDeCompra,on_delete=models.CASCADE)
    libro=models.ForeignKey(Libro,on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=1) 

class Perfil(models.Model):
    usuario=models.OneToOneField(Usuario,on_delete=models.CASCADE)
    imagenPerfil=models.ImageField(upload_to='imagenes_perfil/',null=True,blank=True,editable=True) 
    biografiaPerfil=models.TextField(max_length=2500)
    areasDeInteres=models.CharField(max_length=1000)
    librosLeidos=models.ManyToManyField(Libro,blank=True,related_name='libros_leidos') 

class Post(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    contenidoPost=models.TextField(max_length=15000)
    timestampPost=models.DateTimeField(auto_now_add=True)
    modificacion_timestampPost=models.DateField(auto_now=True)

class Comentario(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    contenidoComentario=models.TextField(max_length=1000)
    timestampComentario=models.DateTimeField(auto_now_add=True)
    modificacion_timestampComentario=models.DateField(auto_now=True)

class Reporte(models.Model):
    ESTADOS=(
        ('PENDIENTE','Pendiente'),
        ('RESUELTO','Resuelto')
    )
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    comentario=models.ForeignKey(Comentario,on_delete=models.CASCADE,null=True,blank=True)
    motivoReporte=models.CharField(max_length=1000)
    estadoReporte=models.CharField(max_length=10,choices=ESTADOS,default='PENDIENTE')
    timestampReporte=models.DateTimeField(auto_now_add=True)
    modificacion_timestampReporte=models.DateField(auto_now=True)

class Notificacion(models.Model):
    TIPO=(
        ('AVISOS','avisos'),
        ('NUEVO COMENTARIO','nuevo comentario'),
        ('REPORTE','reporte')
    )
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    comentario=models.ForeignKey(Comentario,on_delete=models.CASCADE,null=True,blank=True)
    tipoNotificacion=models.CharField(max_length=17,choices=TIPO,default='AVISOS')
    mensajeNotificacion=models.TextField(max_length=1000)
    estadoVista=models.BooleanField(default=False)