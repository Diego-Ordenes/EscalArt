from typing_extensions import Self
from django.utils import timezone
from enum import unique
from lib2to3.pytree import Base
from mailbox import mbox
from operator import truediv
from pyexpat import model
from tabnanny import verbose
from tkinter import CASCADE
from turtle import Turtle
from webbrowser import get
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.test import TransactionTestCase
from requests import request
from taggit.managers import TaggableManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# from typing_extensions import Self

# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombre,tipoCuenta,password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')
        
        usuario = self.model(
            username=username,
            email= self.normalize_email(email),
            nombre =nombre,
            tipoCuenta = TipoCuenta.objects.get(idTipoCuenta =tipoCuenta)
        )
        

        usuario.set_password(password)
        usuario.save()
        

        return usuario
    
    
    def create_superuser(self,username,email,nombre,tipoCuenta,password):
        usuario = self.create_user(
            email,
            username=username,
            nombre=nombre,
            tipoCuenta = tipoCuenta,
            password=password

        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario


# class Categoria(models.Model):
#     idCategoria = models.AutoField(primary_key=True,verbose_name='Id Categoría')
#     nombreCategoria = models.CharField(max_length=50,verbose_name='Nombre Categoría')

#     def __str__(self):
#         return  self.nombreCategoria

class TipoCuenta(models.Model):
    idTipoCuenta = models.AutoField(primary_key=True, verbose_name='Id Tipo Cuenta')
    tipoCuenta = models.CharField(max_length=50,verbose_name='Tipo Cuenta')

    def __str__(self):
        return  self.tipoCuenta

class Usuario(AbstractBaseUser):
    idUser = models.AutoField(primary_key=True,verbose_name='Id Usuario')
    username = models.CharField('Nombre de usuario', unique=True,max_length=50)
    email = models.EmailField('Correo Electronico',max_length=254,unique=True)
    nombre = models.CharField('Nombre completo', max_length=200, blank=True,null=True)
    imagen = models.ImageField('Foto de Perfil', upload_to=None, max_length=200, blank=True, null=True)
    tipoCuenta = models.ForeignKey(TipoCuenta,on_delete=models.CASCADE,verbose_name='Tipo de cuenta')
    is_active = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombre','tipoCuenta']

    def __str__(self):
        return f'{self.nombre}'

    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador

    
class Publicacion(models.Model):
    idPublicacion = models.AutoField(primary_key= True, verbose_name='Id Publicacion')
    descripcion = models.CharField('Descripcion', max_length=250, blank=True,null=True)
    titulo = models.CharField('Titulo Publicacion', max_length=150)
    imagen = models.ImageField('Imagen', upload_to=None, max_length=200, blank = False, null = False)
    cantLikes = models.ManyToManyField(Usuario,blank=True,verbose_name='likes',related_name='likes')
    idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Id Usuario')
    tags = TaggableManager(blank=True)
    fechaCreacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.titulo,self.idUser}'

class Perfil(models.Model):
    idPerfil = models.AutoField(primary_key = True, verbose_name = 'Id Perfil')
    # seguidos = models.ManyToManyField(Usuario, blank=True, related_name='seguidos',verbose_name='nro Seguidos')
    seguidores = models.ManyToManyField(Usuario, blank=True, related_name='seguidores',verbose_name='nro seguidores')
    calificacion = models.IntegerField('Calificacion')
    img_header = models.ImageField('Header', upload_to='index', max_length=200, blank=True, null=True)
    biografia = models.CharField('Biografia', max_length=250, blank=True,null=True)
    idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Id user',unique = True)
    showTags = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f'{self.idPerfil,self.idUser}'

# class Usuario_Categoria(models.Model):
#     idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Id user')
#     idCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Id Categoria')

#     def __str__(self):
#         return f'{self.idUser,self.idCategoria}'

# class Publicacion_Categoria(models.Model):
#     idCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Id Categoria')
#     idPublicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, verbose_name='Id Publicacion')

#     def __str__(self):
#         return f'{self.idPublicacion,self.idCategoria}'

class Comentarios(models.Model):
    comentario = models.CharField('Comentario', max_length=250)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    cantLikes = models.ManyToManyField(Usuario,blank=True,verbose_name='likes',related_name='CommentLikes')
    idPublicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, verbose_name='Id Publicacion')
    idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Id user')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='+')


    def __str__(self):
        return f'{self.idUser,self.comentario}'

    @property
    def children(self):
        return Comentarios.objects.filter(parent=self).order_by('-fechaCreacion').all()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True       
        return False

class EstadoComision(models.Model):
    idEstado = models.AutoField(primary_key=True, verbose_name='Id Estado Comision')
    estado = models.CharField('Estado',max_length=150)
    def __str__(self):
        return f'{self.estado}'

class Comision(models.Model):
    idComision = models.AutoField(primary_key=True, verbose_name='Id Comision')
    idEstado = models.ForeignKey(EstadoComision,on_delete=models.CASCADE,verbose_name='Id Estado Comision')
    idArtista = models.ForeignKey(Usuario,on_delete=models.CASCADE, verbose_name='Id Artista')
    def __str__(self) :
        return f'{self.idComision,self.idArtista,self.idEstado.estado}'

class Comision_Cliente(models.Model):
    idComision = models.ForeignKey(Comision,primary_key=True,on_delete=models.CASCADE,verbose_name='Id Comision')
    idCliente = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Id Cliente')
    def __str__(self) :
        return f'{self.idComision,self.idCliente}'


class Solicitud(models.Model):
    idSolicitud = models.CharField(primary_key=True,verbose_name='Id Solicitud',max_length=150)
    idCliente = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Id Cliente')
    usernameArtista = models.CharField('Username Artista',max_length=150)

    def __str__(self):
        return f'{self.idCliente,self.usernameArtista}'

class Referencia(models.Model):
    idReferecia = models.AutoField(primary_key=True,verbose_name='Id Referencia')
    img_referencia = models.ImageField('Referencia', upload_to='index', max_length=200)
    usernameArtista = models.CharField('Username Artista',max_length=150)
    idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Id Cliente')

    def __str__(self):
        return f'{self.img_referencia,self.idUser,self.usernameArtista}'

class Guardado(models.Model):
    idGuardado = models.CharField(primary_key=True,verbose_name='Id Guardado',max_length=150)
    idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name='Id usuario')
    idPublicacion = models.ForeignKey(Publicacion,on_delete=models.CASCADE,verbose_name='Id publicacion')

    def __str__(self):
        return f'{self.idUser,self.idPublicacion}'


class Review(models.Model):
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    review = models.TextField(max_length=500,blank=True)
    rating = models.IntegerField()
    fechaCreacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.rating}'

class Review_cliente(models.Model):
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    review = models.TextField(max_length=500,blank=True)
    rating = models.IntegerField()
    fechaCreacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.rating}'


class Chat(models.Model):
    contenido = models.CharField(max_length=1000)
    img_referencia = models.ImageField('Referencia', upload_to=None, max_length=200, blank=True, null=True)
    fecha = models.DateTimeField(auto_now=True)
    idUser = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom',on_delete=models.CASCADE)

class ChatRoom(models.Model):
    nombre = models.CharField(max_length=255)
    