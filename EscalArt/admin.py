from django.contrib import admin
from .models import Chat, ChatRoom, Comentarios, Guardado, Perfil, Publicacion,  Referencia, TipoCuenta, Usuario, Comision,Comision_Cliente,EstadoComision
from .models import Solicitud,Review
# Register your models here.


# admin.site.register(Categoria)
admin.site.register(TipoCuenta)
admin.site.register(Usuario)
admin.site.register(Publicacion)
admin.site.register(Perfil)
# admin.site.register(Publicacion_Categoria)
# admin.site.register(Usuario_Categoria)
admin.site.register(Comentarios)
admin.site.register(Comision)
admin.site.register(Comision_Cliente)
admin.site.register(EstadoComision)
admin.site.register(Solicitud)
admin.site.register(Referencia)
admin.site.register(Guardado)
admin.site.register(Review)
admin.site.register(Chat)
admin.site.register(ChatRoom)




