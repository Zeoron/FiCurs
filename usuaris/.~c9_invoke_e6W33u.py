# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import Login_form, Signup_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def p_inicial(request):
    return render(request, 'index.html')


#VISTA PARA LOGUEAR A LOS USUARIOS

def vista_login(request):
    if request.method=='POST': #SI LO ENVIADO ES UN POST...
        form = Login_form(request.POST) #Captura del formulari
        if form.is_valid(): #METODO QUE DICE QUE EL FORMULARIO ES VALIDO (POR NO ENTRADO, SIMBOLOS, LETRAS EN LUGAR DE NUMEROS...)
            username = form.cleaned_data['username'] #Captura el nombre de usuario del formulario
            password = form.cleaned_data['password'] #Captura el padsword del formulario
            seguent = request.GET.get('next', default=None)  #Captura una posible continuación del usuario (donde queria ir)
            user = authenticate(username=username, password=password)  #Si NO es nada...
            if user is not None: #Si existe el usuario...
                if user.is_active: #Si esta activo ...
                    login(request, user) #Autentifica el usuario
                    if bool( seguent ): #Si estava en una url y le ha pedido autentificació
                        return HttpResponseRedirect( seguent ) #Rediridige al usuario donde queria ir
                    else:
                        return HttpResponseRedirect( reverse( 'inicial' ))  #Lo envias a la pagina que tu quieras
                else: #Error en el usuario, no esta activo
                    return HttpResponse("Usuari correcte pero no actiu")
            else: #El usuario no es correcto
                return HttpResponse("Error amb l'usuari!")
    else: #No es un post, genera el formulario
        form = Login_form()
    return render(request, 'login.html', {'form':form}) #Renderiza el formulario en el login.html

def vista_signup(request):
    if request.method == 'POST':
        form = Signup_form(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            usuari = User()
            usuari.username = username
            usuari.set_password(password)
            usuari.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            hola = "Hola"
    else:
        form = Signup_form()
    
    return render(request, 'registre.html', { 'form': form })
    
    
def vista_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def cmpro