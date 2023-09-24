from django.urls import path
from django.contrib.auth import views as auth_views
# from .views import  AddFollower, AddLike, AddLikeComment, CategoriaSearch, RemoveFollower, ResponderComentarioView, Room, UserSearch, cambiar_pass, chats, configuracion, delete_comision, estadoComisionArt, estadoComisionCli, home , ayudacliente,  perfil_cliente, presentacion, publicacion, publicacionHome, seleccionarC, tagged
# from .views import perfil
# from .views import RegistrarUsuario,ayudacliente,delete_publicacion,datosCliente
from .views import *


urlpatterns =[
    path('',home, name="home"),
    path('perfil/<id>',perfil, name="perfil"),
    path('registro/',RegistrarUsuario,name="registro"),
    path('ayudacliente',ayudacliente,name="ayudacliente"),
    path('perfil/<artista>/publicacion/<post>',publicacion,name="publicacion"),
    path('home/<artista>/publicacion/<post>',publicacionHome,name="publicacionHome"),
    path('perfilCli/<id>',perfil_cliente,name="perfil_cliente"),
    path('borrar-publicacion/<id>',delete_publicacion,name='delete_publicacion'),
    path('publicacion/<int:pk>/like',AddLike.as_view(),name='LikePublicacion'),
    path('perfil/<id>/followers/add', AddFollower.as_view(),name='add-follower'),
    path('perfil/<id>/followers/remove', RemoveFollower.as_view(),name='remove-follower'),
    path('buscar/',UserSearch.as_view(),name='buscar-perfil'),
    path('tag/<slug:slug>/', tagged, name="tagged"),
    path('comentario/<int:pk>/like',AddLikeComment.as_view(),name='likeComment'),
    path('perfil/<artista>/publicacion/<int:post_pk>/comentario/<int:pk>/responder',ResponderComentarioView.as_view(),name='responder-comentario'),
    path('chat',chats.as_view(),name="chats"),    
    path('chat/<str:room_name>/',Room.as_view(),name='room'),
    path('datosCliente/<id>',datosCliente,name="datosCliente"),
    path('datosCliente/<idCliente>/comision/<idComision>',estadoComisionArt,name='estadoComisionArt'),
    path('borrar-comision/<id>',delete_comision,name='delete_comision'),
    path('perfilCli/<id>/comision/<idComision>',estadoComisionCli,name='estadoComisionCli'), 
    path('sobre_nosotros',sobre_nosotros,name="sobre_nosotros"),

    path('configuracion',configuracion.as_view(),name="configuracion"),
    path('buscarcategoria/',CategoriaSearch.as_view(),name='buscar-categoria'),

    path('seleccionarC',seleccionarC,name="seleccionarC"),
    path('presentacion',presentacion,name="presentacion"),
    path('configuracion/cambiar_pass',cambiar_pass.as_view(),name="cambiar_pass"),
    path('accounts/password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/cambiar_contra_done.html'),name="cambiar_pass_done"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="registration/cambiar_pass.html"),name='reset_password'),
    path('accounts/password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="registration/cambiar_pass_sent.html"),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/cambiar_pass_form.html"),name='password_reset_confirm'),
    path('accounts/reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/cambiar_pass_done.html"), name='password_reset_complete'),
    
]
