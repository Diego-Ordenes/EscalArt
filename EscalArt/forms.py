from cProfile import label
from dataclasses import field, fields
from socket import fromshare
from tkinter import Widget
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from requests import RequestException, request
from .models import Chat, Review,Comentarios, Comision, Comision_Cliente, EstadoComision, Guardado, Perfil, Publicacion, Referencia, Review_cliente, Usuario,Solicitud

# class CustomUserCreationForm(UserCreationForm):
#     pass

#FORMULARIO REGISTRO V

class FormularioUsuario(forms.ModelForm):
    # Formulario de registro de un usuario en la base de datos
    # variables:
    #     -password1: contrasenna
    #     -password2: verificacion de la contrasenna

    password1 = forms.CharField(max_length = 50,
        min_length = 8,label = 'Contrasenna',widget = forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Ingrese su contrasenna',
            'id':'password1',
            'required':'required',
        }
    ))
    password2 = forms.CharField(max_length = 50,
        min_length = 8,label = 'Contrasenna de confirmacion',widget = forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Confirme contrasenna',
            'id':'password2',
            'required':'required',
        }
    ))
    username = forms.CharField(
        max_length = 50,
        min_length = 6,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Ingrese su usuario',
            }
        )
    )

    class Meta:
        model= Usuario
        fields = ('username','email','nombre','tipoCuenta')
        widgets = {
            
            'email':forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo Electronico',
                }
            ),
            'nombre':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su nombre',
                }
            ),
            'tipoCuenta':forms.RadioSelect(
                attrs={
                    'class':'form_radio-input',
                    
                }                
            )

        }
    

    def clean_password2(self):
        #validacion contrasenna
        # 
        #metodo que valida que mabas contrasennas ingresadas sean igual, esto ates
        # de ser encriptadas y guardadas en la base de datos, retornar contrasenna valida
        # 
        # excepciones: validationError -- cuando las contrasennas no son iguales muestra un mensaje de error

        password1 = self.cleaned_data.get('password1') 
        password2 = self.cleaned_data.get('password2') 

        if password1 != password2:
            raise forms.ValidationError('Contrasennas no coinciden!')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# class PerfilForm(forms.ModelForm):
#     class Meta:
#         model = Perfil
#         fields = ['seguidos','seguidores','calificacion','biografia','idUser']


class publicacionForm(forms.ModelForm):
    
    
    
    
    class Meta:
        model=Publicacion
        fields = ['descripcion','titulo','imagen','tags']
        exclude = ['idUser','imagen','cantLikes']
        widgets = {
            'titulo':forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese un titulo',
                    'id':'titulo-post'
                
                }
            ),
            'descripcion':forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingresa una descripcion',
                    'id':'descripcion-post',
                    
                }
            ),
            
        
        }


class perfilForm(ModelForm):
    # seguidos = forms.IntegerField(initial = 0)
    # seguidores = forms.IntegerField(initial = 0)
    calificacion = forms.IntegerField(initial = 0)
   

    class Meta:
        model = Perfil
        fields = ['calificacion','idUser']
        exclude = ['idUser','biografia','img_header','seguidores']

class calificacionForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['calificacion','idUser']
        exclude = ['idUser']

class editPerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['biografia','img_header']
        exclude = ['img_header']
        widgets = {
            'biografia':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese biografia'
                }
            )

        }

class editFotoPerfilForm(ModelForm):
    class Meta:
        model = Usuario
        fields=['imagen']
        # widgets = {
        #     'imagen': forms.FileInput(),
        # }
        exclude = ['idUser','username','email','nombre','tipoCuenta','usuario_activo','usuario_administrador','objects']
    
class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['idCliente','usernameArtista','idSolicitud']
        exclude = ['idCliente','usernameArtista','idSolicitud']
        
class ComisionArtistaForm(ModelForm):    

    class Meta:
        model = Comision
        fields = ['idEstado','idArtista']
        exclude = ['idEstado','idArtista']

class EditComArtForm(ModelForm):
    class Meta:
        model = Comision
        fields = ['idEstado','idArtista']
        exclude = ['idArtista']

class ComisionClienteForm(ModelForm):
    class Meta:
        model = Comision_Cliente
        fields = ['idComision','idCliente']
        exclude = ['idComision','idCliente']

class ReferenciasForm(ModelForm):
    class Meta:
        model = Referencia
        fields = ['img_referencia','idUser','usernameArtista']
        exclude = ['idUser','usernameArtista']

class GuardarPostForm(ModelForm):
    class Meta:
        model = Guardado
        fields = ['idUser','idPublicacion']
        exclude = ['idUser','idPublicacion']
    

class ComentarioForm(forms.ModelForm):
    comentario = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'rows':'3',
                'placeholder': 'Escribe un comentario...'
            }
        )
    )
    class Meta:
        model = Comentarios
        fields=['comentario']
         

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']

class ReviewClienteForm(forms.ModelForm):
    class Meta:
        model = Review_cliente
        fields = ['review', 'rating']


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['img_referencia']
        exclude = ['idUser','room']


class EditUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre','email','username']
        exclude = ['idUser','imagen','tipoCuenta','email','username']

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['tipoCuenta']
        exclude = ['idUser','imagen','nombre','email','username']

# editar tags perfil
class editTagsPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['showTags','tags']
        widgets = {
            'tags':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'separe las categorias con comas',
                    'id':'inputCategorias'
                }
            )

        }
        exclude = ['showTags','tags','idPerfil','idUser']
class agregarTagsForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['tags']
        
# fin editar tags perfil