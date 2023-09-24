from asyncio.windows_events import NULL
from email import message
from hashlib import new
from itertools import count
from tkinter.messagebox import NO
from xml.etree.ElementTree import Comment
from django.db.models import Q
from multiprocessing.spawn import is_forking
from tkinter.tix import Form
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
# from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from taggit.models import Tag
from django.template.defaultfilters import slugify

from EscalArt.forms import ChatForm, ComisionArtistaForm, ComisionClienteForm, EditComArtForm, EditUsuarioForm, ReferenciasForm, ReviewClienteForm, ReviewForm,ComentarioForm, FormularioUsuario, SolicitudForm, TipoUsuarioForm, agregarTagsForm, calificacionForm, editFotoPerfilForm, editPerfilForm, editTagsPerfil, perfilForm, publicacionForm, GuardarPostForm
from .models import Chat, ChatRoom, Comentarios, Comision, Comision_Cliente, EstadoComision, Perfil, Publicacion, Referencia, Review_cliente, Solicitud, TipoCuenta, Usuario, Guardado, Review




# Create your views here.
def ayudacliente(request):
    if(request.user.is_authenticated):
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)
        data = {
            'menuPfp':menuPfp
        }
    else:
        data = {
            
        }

    return render(request,'escalArt/ayudacliente.html',data)
def sobre_nosotros(request):
    if(request.user.is_authenticated):
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)
        data = {
            'menuPfp':menuPfp
        }
    else:
        data = {

        }

    return render(request,'escalArt/sobre_nosotros.html',data)

def perfil_cliente(request,id):
    try:
        user = Usuario.objects.get(username = id)
    except:
        return redirect(to='perfil_cliente', id=request.user.username )
    list = Perfil.objects.all()
    algo = Perfil.objects.get(idUser = request.user)
    guardados = Guardado.objects.filter(idUser = user)
    comisionCli = Comision_Cliente.objects.filter(idCliente = request.user)
    comisionTrabajo = Comision.objects.filter(idArtista = request.user)
    comision = Comision.objects.all()
    menuPfp = Usuario.objects.get(idUser = request.user.idUser)

    data = {
        'userInfo':user,
        "perfil":list,
        'foto':editFotoPerfilForm(instance = user),
        'edit': editPerfilForm(instance = algo),
        'guardados':guardados,
        "comCli":comisionCli,
        'menuPfp':menuPfp,
        'comisionTrabajo':comisionTrabajo,
        'comision':comision,
    }
    if(request.user != user):
        return redirect(to='perfil_cliente', id=request.user.username )
    


    if request.method == "POST":
        if 'fotoPerfil' in request.POST:
            pfp = request.FILES.get('pfp',None)
            if pfp is None:
                print('no se subio un archivo')
            else:
                print('estas editando tu foto de perfil')
                foto = editFotoPerfilForm(request.POST,request.FILES,instance=user)
                if foto.is_valid():
                    obj =foto.save(commit=False)
                    obj.imagen = request.FILES["pfp"]
                    obj.save()
                else:
                    print(foto.errors)
        elif 'EditHeader' in request.POST:
            header = request.FILES.get('header', None)
            if header is None:
                print('no se subio un archivo')
            else:
                perfil = editPerfilForm(request.POST,request.FILES, instance=algo)
                obj2 = algo.biografia
                print('Estas cambiando el header/banner')
                if perfil.is_valid():
                    print(f'primera bio: {obj2}')
                    obj = perfil.save(commit=False)
                    obj.img_header = request.FILES["header"]
                    obj.biografia = obj2
                    obj.save()
                    print(f'segunda bio: {obj.biografia}')

                else:
                    print(perfil.errors)        
        else:
            print('no se hizo ni un post')
    
    return render(request,'escalArt/perfil_cliente.html',data)

def perfil(request,id):
    
    artista = Usuario.objects.get(username = id)
    reviewForm = ReviewForm()
    if artista.tipoCuenta.tipoCuenta == 'cliente':    
        return redirect(to='perfil_cliente', id=request.user.username )
    post = Publicacion.objects.order_by('-idPublicacion').all()
    list = Perfil.objects.all()
    listArtista = Usuario.objects.all()
    usuario = Perfil.objects.get(idUser = artista.idUser)
    print(usuario.idUser.idUser)
    
    followers =  usuario.seguidores.all()

    following = Perfil.objects.filter(seguidores= artista.idUser )
    following_count = len(following)
    print(f'cuenta de siguiendo = {following_count}')

    if len(followers) ==0:
        is_following = False

    try:
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
    except:
        is_following = False

    
    try:
        reviews = Review.objects.filter(idPerfil = usuario).order_by('-fechaCreacion')
        rating= reviews.values("rating")
        print(f'ayuda: {rating}')
        cant_datos = len(reviews)
        print(cant_datos)
        suma = 0
        for i in rating:
            print(f'i es: {i}')
            i = i.get('rating')
            suma = suma + i
            print(f'suma for = {suma}')
        print(suma)    
         
          
            
        promedio = suma/cant_datos
        calificacion = round(promedio)

    except:
        calificacion = 0


    numero_de_seguidores = len(followers)   

    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)

        menuPfp = Usuario.objects.get(idUser = request.user.idUser)
        
        

        data = {
            "list":artista,
            "posts":post,

            'form':publicacionForm(),
            'perfil':list,
            'edit': editPerfilForm(instance = algo),
            'foto':editFotoPerfilForm(instance = user),
            "listArt":listArtista,
            # "publi":publi
            'numFollowers':numero_de_seguidores,
            'is_following': is_following,
            'following_count':following_count,
            'reviewForm':reviewForm,
            'calificacion':calificacion,
            'perfilform':calificacionForm(instance = usuario),
            'reviews':reviews,
            'solicitudForm': SolicitudForm(),
            'menuPfp':menuPfp,

        }
    else:
        data = {
            "list":artista,

            "posts":post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,
            'numFollowers':numero_de_seguidores,
            'is_following': is_following,
            'reviewForm':reviewForm,
            'calificacion':calificacion,
            'perfilform':calificacionForm(instance = usuario),

            'reviews':reviews,
            'following_count':following_count,


            # "publi":publi
        }

    if(request.method=='POST' ):       
        if 'publicar' in request.POST:
            post = request.FILES.get('publi', None)
            print(f'post = {post}')
            
            if post is None:
                print('ayuda algo paso con lo de la imagen :C')
            else:
                print('estas publicando')

                formulario = publicacionForm(request.POST,request.FILES)   


                if formulario.is_valid():
                    publi = formulario.save(commit=False)
                    publi.idUser = request.user
                    publi.imagen = request.FILES.get('publi')
                    
                    publi.save()
                    formulario.save_m2m()
                            
                else:
                    
                    print(formulario.errors)
            
        elif 'editar' in request.POST:
            
            perfil = editPerfilForm(request.POST,request.FILES,instance=algo)
            print('estas editando')
            if perfil.is_valid():
                perfil.save()
            else:
                print(perfil.errors)
        elif 'EditHeader' in request.POST:
            header = request.FILES.get('header', None)
            if header is None:
                print('no se subio un archivo')
            else:
                perfil = editPerfilForm(request.POST,request.FILES, instance=algo)
                obj2 = algo.biografia
                print('Estas cambiando el header/banner')
                if perfil.is_valid():
                    print(f'primera bio: {obj2}')
                    obj = perfil.save(commit=False)
                    obj.img_header = request.FILES["header"]
                    obj.biografia = obj2
                    obj.save()
                    print(f'segunda bio: {obj.biografia}')

                else:
                    print(perfil.errors)
        elif 'fotoPerfil' in request.POST:
            pfp = request.FILES.get('pfp',None)
            if pfp is None:
                print('no se subio un archivo')
            else:
                print('estas editando tu foto de perfil')
                foto = editFotoPerfilForm(request.POST,request.FILES,instance=user)
                if foto.is_valid():
                    obj =foto.save(commit=False)
                    obj.imagen = request.FILES["pfp"]
                    obj.save()
                else:
                    print(foto.errors)
        elif 'enviarReview' in request.POST:
            if (request.user.is_authenticated):
                review = ReviewForm(request.POST)
                perfil = calificacionForm(request.POST, instance = usuario)
                

                if review.is_valid():
                    obj = review.save(commit=False)
                    obj.idPerfil = usuario
                    obj.idUser = request.user
                    obj.review = request.POST['review']
                    obj.rating = request.POST['rating']
                    obj.save()

                    reviews = Review.objects.filter(idPerfil = usuario)
                    rating= reviews.values("rating")
                    # print(f'ayuda: {rating}')
                    cant_datos = len(reviews)
                    # print(cant_datos)
                    suma = 0
                    for i in rating:
                        # print(f'i es: {i}')
                        i = i.get('rating')
                        suma = suma + i
                        # print(f'suma for = {suma}')
                    print(f'post suma = {suma}')   
                    promedio = suma/cant_datos
                        
                    data['calificacion'] =round(promedio)
                    if perfil.is_valid():  
                        profile = perfil.save(commit=False)                    
                        
                        profile.calificacion = request.POST['calificacion']
                        profile.calificacion = round(promedio)
                        profile.save()
                        data['reviews'] = Review.objects.filter(idPerfil = usuario).order_by('-fechaCreacion')
                    else:
                        print(perfil.errors)                
                else:
                    print(review.errors)
            else:
                messages.error('Tienes que estar loggeado para hacer esto')
        elif 'solicitud' in request.POST:
            if (request.user.is_authenticated):
                form = SolicitudForm(request.POST)
            
                if form.is_valid():
                    obj = form.save(commit = False)
                    obj.idSolicitud = f"{request.user.username}{artista.username}"
                    obj.idCliente = request.user
                    obj.usernameArtista = artista.username
                    obj.save()
                    # return render(request,'escalArt/mensajes.html',data)
                else:
                    print(form.errors)
            else:
                data['message'] = 'Error. Debes estar loggeado con una cuenta para realizar esta accion'
        else:
            print('no se hizo ni un post')        
    
    return render(request, 'escalArt/Perfil_Artista.html',data)

def publicacion(request,artista,post):
    comentarios = Comentarios.objects.filter(idPublicacion = post).order_by('-fechaCreacion')
    Artista = Usuario.objects.get(username = artista)
    publi = Publicacion.objects.get(idPublicacion = post)
    if(artista != publi.idUser.username):
        return redirect(to='publicacion', artista=publi.idUser.username, post = post )

    commentForm = ComentarioForm()
    Post = Publicacion.objects.all()
    list = Perfil.objects.all()
    listArtista = Usuario.objects.all()
    try:
        guardado = Guardado.objects.get(idPublicacion = post, idUser = request.user)

        
    except:
        guardado = None
        print('no se ha guardado la publicacion aun')      
    

    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)

        if guardado is None:
            data = {
                "list":Artista,
                "posts":Post,

                'form':publicacionForm(),
                'perfil':list,
                'edit': editPerfilForm(instance = algo),
                'foto':editFotoPerfilForm(instance = user),
                "listArt":listArtista,
                "publi":publi,
                'guardarPost':GuardarPostForm(),
                'commentForm':commentForm,
                'comentarios':comentarios,
                'menuPfp':menuPfp,

            }
        else:
            data = {
                "list":Artista,
                "posts":Post,

                'form':publicacionForm(),
                'perfil':list,
                'edit': editPerfilForm(instance = algo),
                'foto':editFotoPerfilForm(instance = user),
                "listArt":listArtista,
                "publi":publi,
                'guardarPost':GuardarPostForm(),
                'guardado':guardado,
                'commentForm':commentForm,
                'comentarios':comentarios,
                'menuPfp':menuPfp,

            }
    else:
        data = {
            "list":Artista,

            "posts":Post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,

            "publi":publi,
            'comentarios':comentarios,
            'commentForm':commentForm,

        }
    
    if request.method == 'POST':
        
        if 'guardarPost' in request.POST:
            guardarPost = GuardarPostForm(request.POST)
            if guardarPost.is_valid:
                obj = guardarPost.save(commit=False)
                obj.idGuardado = f'{request.user}-{request.POST["idPost"]}'
                obj.idUser = request.user
                obj.idPublicacion = Publicacion.objects.get(idPublicacion = request.POST["idPost"])
                print(obj.idPublicacion)
                obj.save()
                data['guardado'] = Guardado.objects.get(idPublicacion = obj.idPublicacion, idUser = request.user)
            else:
                print(guardarPost.errors)
        
        elif 'eliminarPostGuardado' in request.POST:
            guardado = Guardado.objects.get(idPublicacion=post, idUser = request.user)
            guardado.delete()
            data['guardado'] = None
        elif 'comentar' in request.POST:
            comentario = ComentarioForm(request.POST)
            if comentario.is_valid:
                nuevo_comentario = comentario.save(commit=False)
                nuevo_comentario.idUser = request.user
                nuevo_comentario.idPublicacion = publi
                nuevo_comentario.save()
            else:
                print(comentario.errors)
        else:
            ('ningun post ha coincidido')

    else:
        print('no se ha hecho ni un post')
    
    return render(request,'escalArt/publicacion.html',data)


def publicacionHome(request,artista,post):
    Artista = Usuario.objects.get(username = artista)
    publi = Publicacion.objects.get(idPublicacion = post)
    guardados = Guardado.objects.all()
    comentarios = Comentarios.objects.filter(idPublicacion = post).order_by('-fechaCreacion')
    commentForm = ComentarioForm()
    listArtista = Perfil.objects.all().annotate(followers=Count('seguidores')).order_by('-followers')[:4]

        

   

    try:
        guardado = Guardado.objects.get(idPublicacion = post, idUser = request.user)

        
    except:
        guardado = None
        print('no se ha guardado la publicacion aun')

    Post = Publicacion.objects.all()
    list = Perfil.objects.all()
    listaUsuarios = Usuario.objects.all()
    print(f'guardado 2 = {guardado}')
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)

        if guardado is None:
            data = {
                "list":Artista,
                "posts":Post,

                'form':publicacionForm(),
                'perfil':list,
                'edit': editPerfilForm(instance = algo),
                'foto':editFotoPerfilForm(instance = user),
                "listArt":listArtista,
                'listaUsuarios':listaUsuarios,
                "publi":publi,
                'guardarPost':GuardarPostForm(),
                'guardados':guardados,
                'comentarios':comentarios,
                'commentForm':commentForm,
                'menuPfp':menuPfp,


            }
        else:
            data = {
                "list":Artista,
                "posts":Post,

                'form':publicacionForm(),
                'perfil':list,
                'edit': editPerfilForm(instance = algo),
                'foto':editFotoPerfilForm(instance = user),
                "listArt":listArtista,
                "publi":publi,
                'guardarPost':GuardarPostForm(),
                'guardados':guardados,
                'guardado':guardado,    
                'comentarios':comentarios,
                'listaUsuarios':listaUsuarios,
                'commentForm':commentForm,
                'menuPfp':menuPfp,
                          
            }
            
    else:
        data = {
            "list":Artista,

            "posts":Post,

            'form':publicacionForm(),
            'perfil':list,
            "listArt":listArtista,

            "publi":publi,
            'comentarios':comentarios,
            'listaUsuarios':listaUsuarios,
            'commentForm':commentForm,
           
        }
    
    if request.method == 'POST':
        if 'guardarPost' in request.POST:
            guardarPost = GuardarPostForm(request.POST)
            if guardarPost.is_valid:
                obj = guardarPost.save(commit=False)
                obj.idGuardado = f'{request.user}-{request.POST["idPost"]}'
                obj.idUser = request.user
                obj.idPublicacion = Publicacion.objects.get(idPublicacion = request.POST["idPost"])
                print(obj.idPublicacion)
                obj.save()
                data['guardado'] = Guardado.objects.get(idPublicacion = obj.idPublicacion, idUser = request.user)
            else:
                print(guardarPost.errors)
        
        elif 'eliminarPostGuardado' in request.POST:
            guardado = Guardado.objects.get(idPublicacion = post, idUser = request.user)

            guardado.delete()
            data['guardado'] = None

        elif 'comentar' in request.POST:
            comentario = ComentarioForm(request.POST)
            if comentario.is_valid:
                nuevo_comentario = comentario.save(commit=False)
                nuevo_comentario.idUser = request.user
                nuevo_comentario.idPublicacion = publi
                nuevo_comentario.save()
            else:
                print(comentario.errors)
        else:
            ('ningun post ha coincidido')
        
    else:
        print('no se ha hecho ni un post')
    return render(request,'escalArt/publicacionHome.html',data)


class ResponderComentarioView(View):
    def post(self,request,artista,post_pk,pk,*args,**kwargs):
        post = Publicacion.objects.get(idPublicacion = post_pk)

        parent_comment = Comentarios.objects.get(pk = pk)
        form = ComentarioForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.idUser = request.user
            new_comment.idPublicacion = post
            new_comment.parent = parent_comment
            new_comment.save()
       
        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)
        
def tagged(request, slug):

    tag = get_object_or_404(Tag, slug=slug)
    
    listArtista = Perfil.objects.all().annotate(followers=Count('seguidores')).order_by('-followers')[:4]

    list = Perfil.objects.all()
    post = Publicacion.objects.filter(tags=tag)
    common_tags = Tag.objects.all()[:10]

    # print(request.user)
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)

        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        
        'edit': editPerfilForm(instance = algo),
        'foto':editFotoPerfilForm(instance = user),

        "listArt":listArtista,
        'common_tags':common_tags,
        'tag':tag,
        'menuPfp':menuPfp,

    }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        "listArt":listArtista,
        'common_tags':common_tags,
        'tag':tag,
        
    
    }
    return render(request, 'escalArt/index.html', data)

from django.db.models import Count
def home (request):
    list = Perfil.objects.all()
    post = Publicacion.objects.all().annotate(likes=Count('cantLikes')).order_by('-likes')[:6]
    listArtista = Perfil.objects.all().annotate(followers=Count('seguidores')).order_by('-followers')[:4]
    common_tags = Tag.objects.all()[:10]
    artistas = Usuario.objects.filter(tipoCuenta = 2)
    print(artistas)
    # print(request.user)
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)

        data = {
            "perfil":list,
            "posts":post,
            'form':publicacionForm(),
            
            'edit': editPerfilForm(instance = algo),
            'foto':editFotoPerfilForm(instance = user),

            "listArt":listArtista,
            'common_tags':common_tags,
            'menuPfp':menuPfp,
        }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        "listArt":listArtista,
        'common_tags':common_tags,        
    
    }

    if(request.method=='POST' ):

        if 'editar' in request.POST:
            perfil = editPerfilForm(request.POST,request.FILES,instance=algo)
            print('estas editando')
            if perfil.is_valid():
                perfil.save()
            else:
                print(perfil.errors)
        elif 'publicar' in request.POST:
            print('estas publicando')
            formulario = publicacionForm(request.POST,request.FILES)
            

            if formulario.is_valid():
                obj = formulario.save(commit=False)
                obj.idUser = request.user
                
                obj.save()
                        
            else:
                print('algo paso wn matate')
                print(formulario.errors)
        elif 'fotoPerfil' in request.POST:
            print('estas editando tu foto de perfil')
            foto = editFotoPerfilForm(request.POST,request.FILES,instance=user)
            if foto.is_valid():
                foto.save()
            else:
                print(foto.errors)
        else:
            print('no se hizo ni un post')
        
    return render(request,'escalArt/index.html',data)


def RegistrarUsuario (request):
    list = Perfil.objects.all()
    post = Publicacion.objects.all().annotate(likes=Count('cantLikes')).order_by('-likes')
    listArtista = Perfil.objects.all().annotate(followers=Count('seguidores')).order_by('-followers')[:4]

    common_tags = Tag.objects.all()[:10]
    # print(request.user)
    if (request.user.is_authenticated):
        algo = Perfil.objects.get(idUser = request.user)
        user = Usuario.objects.get(idUser =  request.user.idUser)
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)

        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        
        'edit': editPerfilForm(instance = algo),
        'foto':editFotoPerfilForm(instance = user),

        "listArt":listArtista,
        'common_tags':common_tags,
        "perfil":perfilForm(),
        'form':FormularioUsuario(),
        'menuPfp':menuPfp,

    }
    else:
        data = {
        "perfil":list,
        "posts":post,
        'form':publicacionForm(),
        "listArt":listArtista,
        'common_tags':common_tags, 
        "perfil":perfilForm(),
        'form':FormularioUsuario(),       
    
    }
   
    if(request.method=='POST' ):
        formulario = FormularioUsuario(request.POST)
        perfil = perfilForm(request.POST)      

        if formulario.is_valid():
            obj = formulario.save(commit=False)
            print(f'id: {obj.nombre}')
            
            if perfil.is_valid():
                obj.save()

                obj2 = perfil.save(commit=False)
                obj2.idUser = Usuario.objects.get(username = obj.username)
                print(f'quesesto: {obj2.idUser}')

                obj2.save()
            else:
                print(perfil.errors)
                exit
            
            return render(request,'escalArt/index.html',data)
                      
        else:
            print('algo paso wn matate')
            print(formulario.errors)
            data['error'] =formulario.errors

            print(perfil.errors)
    return render(request,'registration/registro.html',data)

# Agregar likes
class AddLike(View):
    def post(self, request, pk, *args, **kwargs):
        post = Publicacion.objects.get(idPublicacion = pk)
        is_liked = False

        for like in post.cantLikes.all():
            if like == request.user:
                is_liked = True
                break
            
        if not is_liked:
            post.cantLikes.add(request.user)

        if is_liked:
            post.cantLikes.remove(request.user)

          
        
        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)

class AddLikeComment(View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comentarios.objects.get(pk = pk)
        comment_liked = False

        for like in comment.cantLikes.all():
            if like == request.user:
                comment_liked = True
                break
            
        if not comment_liked:
            comment.cantLikes.add(request.user)

        if comment_liked:
            comment.cantLikes.remove(request.user)    
        
        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)

# Fin agregar likes
# Follows
class AddFollower(View):
    def post(self,request,id,*args,**kwargs):
        profile = Perfil.objects.get(idUser = id)
        profile.seguidores.add(request.user)

        return redirect('perfil', id = profile.idUser.username)

class RemoveFollower(View):
    def post(self,request,id,*args,**kwargs):
        profile = Perfil.objects.get(idUser = id)
        profile.seguidores.remove(request.user)

        return redirect('perfil', id = profile.idUser.username)
# Fin follows
# Buscar
class UserSearch(View):
    def get(self,request,*args,**kwargs):
        try:
            usuarios = Usuario.objects.all()
            query = self.request.GET.get('query')
            
            if Q(idUser__username__icontains = query):
                lista_perfilUsername = Perfil.objects.filter(
                    Q(idUser__username__icontains = query)
                )
                print(f'perfiles segun username: {lista_perfilUsername}')
                
            
            if Q(idUser__nombre__icontains = query):
                lista_perfil = Perfil.objects.filter(
                    Q(idUser__nombre__icontains = query)
                )
                print(f'perfiles segun nombre: {lista_perfil}')

            if Q(tags__name__icontains = query):
                lista_post = Publicacion.objects.filter(
                    Q(tags__name__icontains = query)
                )
                lista_perfil_tag = Perfil.objects.filter(
                    Q(tags__name__icontains = query)
                )
            post_list = []
            for post in lista_post:
                if post in post_list:
                    pass
                else:
                    post_list.append(post)
            lista_post = post_list
            print(f'lista posts: {lista_post}')

            lista_perfilNombre = []
            for perfil in lista_perfil:
                print(perfil)
                print(perfil.idUser.tipoCuenta)
                if (str(perfil.idUser.tipoCuenta) == 'artista'):
                    lista_perfilNombre.append(perfil)
                else:
                    print('no ingreso al if ???')
                print(lista_perfilNombre)
            lista_perfil = lista_perfilNombre

            lista_perfil_usernames = []
            for perfil in lista_perfilUsername:
                print(perfil)
                print(perfil.idUser.tipoCuenta)
                if (str(perfil.idUser.tipoCuenta) == 'artista'):
                    lista_perfil_usernames.append(perfil)
                else:
                    print('no ingreso al if ??? usernames')
                print(lista_perfilUsername)
            lista_perfilUsername = lista_perfil_usernames

            
        except:
            lista_perfil = None
            lista_post = None
            lista_perfil_tag = None
            lista_perfilUsername = None
        
        print(f'perfiles-username: {lista_perfilUsername}')
        print(f'perfiles-nombre: {lista_perfil}')
        if(request.user.is_authenticated):
            menuPfp = Usuario.objects.get(idUser = request.user.idUser)

            
            data = {
                'lista_perfil':lista_perfil,
                'lista_post':lista_post,
                'lista_perfil_tag':lista_perfil_tag,
                'lista_perfilUsername':lista_perfilUsername,
                'menuPfp':menuPfp,
            }
        else:
            data = {
                'lista_perfil':lista_perfil,
                'lista_post':lista_post,
                'lista_perfil_tag':lista_perfil_tag,
                'lista_perfilUsername':lista_perfilUsername,

            }
        return render(request, 'escalArt/search.html',data)
class CategoriaSearch(View):
    def get(self,request,*args,**kwargs):
        usuario = Usuario.objects.get(idUser = request.user.idUser)    
        if usuario.tipoCuenta.tipoCuenta == 'cliente':
            return redirect(to='configuracion')    
        common_tags = Tag.objects.all().order_by('name')[:10]
        perfilUser = Perfil.objects.get(idUser = request.user)
        Notags =[]
        tagPerfil = perfilUser.tags.all()
        # print(tagPerfil)
        
        for ctags in common_tags:
            # print(ctags)
            if (ctags in tagPerfil):
                # print('a')
                pass
            else:
                Notags.append(ctags)
                # print(Notags)

             

        try:
            query = self.request.GET.get('query')            
            
            lista_tag = []
            tag = Tag.objects.filter(name = query) 
            obj = tag.values('name')
            for i in obj:
                i = i.get('name')
                print(i)
                lista_tag.append(i)
            
        except:
            lista_tag = []
        
        tagsPerfil = []
        tagPerfil = perfilUser.tags.all()
        tag= tagPerfil.values("name")
        for i in tag:
            i = i.get('name')
            print(i)
            tagsPerfil.append(i)
        exists = False
        for ltag in lista_tag:
            if ltag in tagsPerfil:
                exists = True
            else:
                exists = False
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)
        
        data = {
            'lista_tag':lista_tag,
            'usuario':usuario,
            'common_tags':common_tags,
            'perfil':perfilUser,
            'Notags':Notags,
            'existe':exists,
            'menuPfp':menuPfp,
        }
        return render(request, 'escalArt/searchCategorias.html',data)
    def post(self,request,*args,**kwargs):
        usuario = Usuario.objects.get(idUser = request.user.idUser)
        perfilUser = Perfil.objects.get(idUser = request.user)
        common_tags = Tag.objects.all().order_by('name')[:10]

        if request.method == "POST":
            if 'editarPerfil' in request.POST:
                cuenta = EditUsuarioForm(request.POST,instance=usuario)               
                if request.POST['username']:
                    username = request.POST['username']
                else:
                    username = usuario.username
                if request.POST['nombre']:
                    nombre = request.POST['nombre']
                else:
                    nombre = usuario.nombre
                if request.POST['email']:
                    email = request.POST['email']
                else:
                    email = usuario.email              
               
               
                if cuenta.is_valid():
                    obj = cuenta.save(commit=False) 
                    obj.nombre = nombre
                    obj.email = email
                    obj.username = username
                    obj.save()                     
                else:
                    print(f'edit usuario errores: {cuenta.errors}')
            
            
            elif 'editarBio' in request.POST:
                perfil = editPerfilForm(request.POST,request.FILES,instance=perfilUser)
                print('estas editando')
                if perfil.is_valid():
                    obj=perfil.save(commit=False)
                    obj.biografia = request.POST['biografia']
                    obj.save()
                else:
                    print(perfil.errors)

            elif 'editPfp' in request.POST:
                pfp = request.FILES.get('pfp',None)
                if pfp is None:
                    print('no se subio un archivo')
                else:
                    foto = editFotoPerfilForm(request.POST,request.FILES,instance=usuario)
                    if foto.is_valid():
                        obj =foto.save(commit=False)
                        obj.imagen = request.FILES["pfp"]
                        obj.save()
                    else:
                        print(foto.errors)
            elif 'editTags' in request.POST:
                tagsForm = editTagsPerfil(request.POST, instance = perfilUser)
                tagsPerfil = []
                tagPerfil = perfilUser.tags.all()
                tag= tagPerfil.values("name")
                for i in tag:
                    i = i.get('name')
                    print(i)
                    tagsPerfil.append(i)
                print(f'tags en perfil: {tagsPerfil}')
                tagsElegidas = request.POST.getlist('tags')
                unCheck = request.POST.get('tags',False)
                
                showTags = request.POST.get('showTags',False)
                print(tagsElegidas)
                print(showTags)
                if tagsForm.is_valid():
                    obj = tagsForm.save(commit=False)
                    if showTags == 'on':
                        obj.showTags = True
                    else:
                        obj.showTags = False

                    try:
                        query = self.request.GET.get('query') 
                        if unCheck is False:
                            perfilUser.tags.remove(query)
                    except:
                        pass

                    for tagElegida in tagsElegidas:
                        if tagElegida in tagsPerfil:
                            print('ya tienes esta tag')
                        else:
                            perfilUser.tags.add(tagElegida)
                    
                    
                    
                    obj.save()
                    tagsForm.save_m2m()
                else:
                    print(f'error en editar tags: {tagsForm.errors}')    
                # if tagsForm
                
            next = request.POST.get('next','/')
        return redirect(to='configuracion')
# Fin buscar
# Chats
class chats(LoginRequiredMixin,View):
    def get(self, request):
        artista = Usuario.objects.get(username = request.user.username)
        cliente = Usuario.objects.all()
        # estadoCom = EstadoComision.objects.get(idEstado = 1)
        solicitud = Solicitud.objects.all()
        referencias = Referencia.objects.all()
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)

        data ={
            'list': artista,
            'sol':solicitud,
            'cli':cliente,
            'comArt':ComisionArtistaForm,
            'comCli':ComisionClienteForm,
            'ref':ReferenciasForm(),
            'refAll': referencias,
            'menuPfp':menuPfp,

        }
        return render(request, 'escalArt/chats.html',data)

class Room(LoginRequiredMixin,View):
    def get(self,request,room_name):
        room = ChatRoom.objects.filter(nombre = room_name).first()
        referencias = Referencia.objects.all()

        chats = []
        if room:
            chats = Chat.objects.filter(room=room).order_by('fecha')
        else:
            room = ChatRoom(nombre = room_name)
            room.save()

        artista = Usuario.objects.get(username = request.user.username)
        cliente = Usuario.objects.all()
        # estadoCom = EstadoComision.objects.get(idEstado = 1)
        solicitud = Solicitud.objects.all()
        referencias = Referencia.objects.all()
        soliCli = Solicitud.objects.get(idSolicitud = room_name)
        # print(f'solicitud = {soliCli.idCliente}')

        # users = soliCli.values("idUser")
        # for user in users:
        #     user = user.get('idCliente')
        #     if (user ==  request.user.idUser):
        #         print('no')
        #     else:
        #         cli = user
        #         break
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)
        

        data ={
            'list': artista,
            'sol':solicitud,
            'cli':cliente,
            'comArt':ComisionArtistaForm,
            'comCli':ComisionClienteForm,
            'ref':ReferenciasForm(),
            'refAll': referencias,
            'room_name':room_name,
            'chats':chats,
            'sala':room,
            'cliente':soliCli,
            'refAll':referencias,
            'menuPfp':menuPfp,
            # 'users':users
        }
        return render(request,'escalArt/pruebaRoom.html',data)
    def post(self,request,room_name,*args,**kwargs):
        estadoCom = EstadoComision.objects.get(idEstado = 1)

        if 'referencia' in request.POST:
            print('estas subiendo una referencia')
            referencia = ReferenciasForm(request.POST,request.FILES)
            soliCli = Solicitud.objects.get(idSolicitud = room_name)
            
           
            if referencia.is_valid():
                ref = referencia.save(commit=False)
                ref.img_referencia = request.FILES['img_referencia']
                ref.usernameArtista = soliCli.usernameArtista
                ref.idUser = request.user
                
                ref.save()                
                              
            else:
                print('algo paso wn matate')
                print(referencia.errors)
        elif 'comision' in request.POST:
            comArt = ComisionArtistaForm(request.POST)
            comCli = ComisionClienteForm(request.POST)
            if comArt.is_valid():
                obj = comArt.save(commit = False)
                obj.idEstado = estadoCom
                obj.idArtista = request.user
                
                if comCli.is_valid():
                    obj.save()
                    obj2= comCli.save(commit=False)
                    obj2.idComision = obj
                    
                    obj2.idCliente = Usuario.objects.get(username = request.POST['cliente'])
                    obj2.save()
                else:
                    print(comCli.errors)
                
                # return render(request,'escalArt/mensajes.html',data)
            else:
                print(comArt.errors)
        

        next = request.POST.get('next','/')

        return HttpResponseRedirect(next)
# Fin chats

# Datos cliente
def datosCliente(request,id):
    if (id == request.user.username):
        return redirect(to='perfil_cliente', id=request.user.username )

    user = Usuario.objects.get(username = id)
    comCli = Comision_Cliente.objects.filter(idCliente = user)
    listaPerfiles = Perfil.objects.all()
    perfil = Perfil.objects.get(idUser = user.idUser)
    referencias = Referencia.objects.all()
    menuPfp = Usuario.objects.get(idUser = request.user.idUser)
    reviews = Review_cliente.objects.filter(idPerfil = perfil.idPerfil)

    data = {
        'userInfo':user,
        "perfiles":listaPerfiles,
        'perfil':perfil,
        'referencias':referencias,
        'comCli':comCli,
        'menuPfp':menuPfp,
        'reviews':reviews,
    }

    if (request.method=='POST'):
        if 'enviarReview' in request.POST:
           
            review = ReviewClienteForm(request.POST)
            

            if review.is_valid():
                obj = review.save(commit=False)
                obj.idPerfil = perfil
                obj.idUser = request.user
                obj.review = request.POST['review']
                obj.rating = request.POST['rating']
                obj.save()

                # reviews = Review.objects.filter(idPerfil = usuario)
                # rating= reviews.values("rating")
                # # print(f'ayuda: {rating}')
                # cant_datos = len(reviews)
                # # print(cant_datos)
                # suma = 0
                # for i in rating:
                #     # print(f'i es: {i}')
                #     i = i.get('rating')
                #     suma = suma + i
                #     # print(f'suma for = {suma}')
                # print(f'post suma = {suma}')   
                # promedio = suma/cant_datos
                    
                # data['calificacion'] =round(promedio)
                              
            else:
                print(review.errors)            
        elif 'comision' in request.POST:
            estadoCom = EstadoComision.objects.get(idEstado = 1)

            comArt = ComisionArtistaForm(request.POST)
            comCli = ComisionClienteForm(request.POST)
            if comArt.is_valid():
                obj = comArt.save(commit = False)
                obj.idEstado = estadoCom
                obj.idArtista = request.user
                
                if comCli.is_valid():
                    obj.save()
                    obj2= comCli.save(commit=False)
                    obj2.idComision = obj
                    
                    obj2.idCliente = Usuario.objects.get(username = request.POST['cliente'])
                    obj2.save()
                else:
                    print(comCli.errors)
                
                # return render(request,'escalArt/mensajes.html',data)
            else:
                print(comArt.errors)
            

            next = request.POST.get('next','/')

            return HttpResponseRedirect(next)

        
            
    return render(request, 'escalArt/datosCliente.html',data)
# Fin datos cliente

# estados comision
def estadoComisionArt(request,idCliente,idComision):

    user = Usuario.objects.get(username = idCliente)
    comCli = Comision_Cliente.objects.filter(idCliente = user)
    comision = Comision_Cliente.objects.get(idComision = idComision)
    listaPerfiles = Perfil.objects.all()
    perfil = Perfil.objects.get(idUser = user.idUser)
    referencias = Referencia.objects.all()
    menuPfp = Usuario.objects.get(idUser = request.user.idUser)
    reviews = Review_cliente.objects.filter(idPerfil = perfil.idPerfil)

    data = {
        'userInfo':user,
        "perfiles":listaPerfiles,
        'perfil':perfil,
        'referencias':referencias,
        'comCli':comCli,
        'comision':comision,
        'form':EditComArtForm(),
        'menuPfp':menuPfp,
        'reviews':reviews,

    }

    if (request.method == 'POST' and 'editar' in request.POST):
        
        comision = Comision.objects.get(idComision = request.POST['comision'])
        comArt = EditComArtForm(request.POST,instance = comision)
        if comArt.is_valid():
            comArt.save()            
       
        else:
            print(comArt.errors)
            
    else:
        print('no esta entrando')
    return render(request, 'escalArt/estadoComisionArt.html',data)


def estadoComisionCli(request,id,idComision):
    try:
        comision = Comision_Cliente.objects.get(idComision = idComision)
    except:
        return redirect(to='perfil_cliente', id=request.user.username )
    try:
        user = Usuario.objects.get(username = id)
    except:
        return redirect(to='perfil_cliente', id=request.user.username )
    list = Perfil.objects.all()
    algo = Perfil.objects.get(idUser = request.user)
    guardados = Guardado.objects.filter(idUser = user)

    comisionCli = Comision_Cliente.objects.filter(idCliente = request.user)
    # comision = Comision_Cliente.objects.get(idComision = idComision)
    menuPfp = Usuario.objects.get(idUser = request.user.idUser)

    data = {
        'userInfo':user,
        "perfil":list,
        'foto':editFotoPerfilForm(instance = user),
        'edit': editPerfilForm(instance = algo),
        'guardados':guardados,
        "comCli":comisionCli,
        'comision':comision,
        'menuPfp':menuPfp,
    }
    if(request.user != user):
        return redirect(to='perfil_cliente', id=request.user.username )
    
    
    return render(request, 'escalArt/estadoComisionCli.html',data)
# fin estados comision

# delete
def delete_comision(request,id):
    comision = Comision.objects.get(idComision = id)
    comCli = Comision_Cliente.objects.get(idComision = comision)
    idCli = comCli.idCliente.username
    comision.delete()
    
    return redirect(to='datosCliente', id=idCli )

def delete_publicacion(request,id):
    post = Publicacion.objects.get(idPublicacion=id)
    post.delete()

    return redirect(to='perfil', id = request.user.username)

#  Fin delete

# Configuraciones

class configuracion (LoginRequiredMixin,View):
    def get(self,request):
        usuario = Usuario.objects.get(idUser = request.user.idUser)        
        common_tags = Tag.objects.all().order_by('name')[:10]
        perfilUser = Perfil.objects.get(idUser = request.user)
        
        Notags =[]
        tagPerfil = perfilUser.tags.all()
        # print(tagPerfil)
        
        for ctags in common_tags:
            # print(ctags)
            if (ctags in tagPerfil):
                # print('a')
                pass
            else:
                Notags.append(ctags)
                # print(Notags)

        menuPfp = Usuario.objects.get(idUser = request.user.idUser)
        
        data = {
            'usuario':usuario,
            'common_tags':common_tags,
            'perfil':perfilUser,
            'Notags':Notags,
            'formTags' : agregarTagsForm(),
            'menuPfp':menuPfp,
        }       

        return render(request,'escalArt/Configuracion.html',data)
    def post(self,request,*args,**kwargs):
        usuario = Usuario.objects.get(idUser = request.user.idUser)
        perfilUser = Perfil.objects.get(idUser = request.user)
        common_tags = Tag.objects.all().order_by('name')[:10]

        if request.method == "POST":
            if 'editarPerfil' in request.POST:
                cuenta = EditUsuarioForm(request.POST,instance=usuario)               
                if request.POST['username']:
                    username = request.POST['username']
                else:
                    username = usuario.username
                if request.POST['nombre']:
                    nombre = request.POST['nombre']
                else:
                    nombre = usuario.nombre
                if request.POST['email']:
                    email = request.POST['email']
                else:
                    email = usuario.email              
               
               
                if cuenta.is_valid():
                    obj = cuenta.save(commit=False) 
                    obj.nombre = nombre
                    obj.email = email
                    obj.username = username
                    obj.save()                     
                else:
                    print(f'edit usuario errores: {cuenta.errors}')
            
            
            elif 'editarBio' in request.POST:
                perfil = editPerfilForm(request.POST,request.FILES,instance=perfilUser)
                print('estas editando')
                if perfil.is_valid():
                    obj=perfil.save(commit=False)
                    obj.biografia = request.POST['biografia']
                    obj.save()
                else:
                    print(perfil.errors)

            elif 'editPfp' in request.POST:
                pfp = request.FILES.get('pfp',None)
                if pfp is None:
                    print('no se subio un archivo')
                else:
                    foto = editFotoPerfilForm(request.POST,request.FILES,instance=usuario)
                    if foto.is_valid():
                        obj =foto.save(commit=False)
                        obj.imagen = request.FILES["pfp"]
                        obj.save()
                    else:
                        print(foto.errors)
            elif 'editTags' in request.POST:
                tagsForm = editTagsPerfil(request.POST, instance = perfilUser)
                tagsPerfil = []
                tagPerfil = perfilUser.tags.all()
                tag= tagPerfil.values("name")
                for i in tag:
                    i = i.get('name')
                    print(i)
                    tagsPerfil.append(i)
                print(f'tags en perfil: {tagsPerfil}')
                tagsElegidas = request.POST.getlist('tags')
                
                showTags = request.POST.get('showTags',False)
                print(tagsElegidas)
                print(showTags)
                if tagsForm.is_valid():
                    obj = tagsForm.save(commit=False)
                    if showTags == 'on':
                        obj.showTags = True
                    else:
                        obj.showTags = False

                    for tagElegida in tagsElegidas:
                        if tagElegida in tagsPerfil:
                            print('ya tienes esta tag')
                        else:
                            perfilUser.tags.add(tagElegida)

                    
                    
                    NotChecked = []
                    tag= common_tags.values("name")                    
                    for ctags in tag:
                        ctags = ctags.get('name')
                        if (ctags in tagsElegidas):
                            print('a')
                            pass
                        else:
                            NotChecked.append(ctags)
                            print(NotChecked)
                    print(f'lista no checked = {NotChecked}')
                    
                    for notTag in NotChecked:
                        if notTag in tagsPerfil:
                            perfilUser.tags.remove(notTag)
                    
                    obj.save()
                    tagsForm.save_m2m()
                else:
                    print(f'error en editar tags: {tagsForm.errors}')    
                # if tagsForm
            elif 'profesional' in request.POST:
                tipoCuentaFrom = TipoUsuarioForm(request.POST,instance=usuario)
                if tipoCuentaFrom.is_valid():
                    obj = tipoCuentaFrom.save(commit=False)
                    obj.tipoCuenta = TipoCuenta.objects.get(idTipoCuenta=request.POST['tipoCuenta'])
                    obj.save()
                else:
                    print(tipoCuentaFrom.errors)
                
            next = request.POST.get('next','/')
        return HttpResponseRedirect(next)
def seleccionarC(request):
    return render(request, 'escalArt/seleccionarC.html')
# Fin Configuraciones
# Cambiar contrasenna
class cambiar_pass(PasswordChangeView,LoginRequiredMixin,View):
    def get(self,request):
        usuario = Usuario.objects.get(idUser = request.user.idUser) 
        menuPfp = Usuario.objects.get(idUser = request.user.idUser)
        
           
        data = {
            'usuario':usuario,
            'menuPfp':menuPfp,
        }      

        return render(request,'registration/cambiar_contra_form.html',data)
        
# Fin cambair contrasenna

# presentacion?
def presentacion(request):
    return render(request, 'escalArt/presentacion.html')
# Fin presentacion?
