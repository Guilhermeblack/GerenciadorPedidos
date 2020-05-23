from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from . import models
from . import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import permission_required, login_required

def index(request):
    if request.user.is_authenticated == False:
        messages.info(request, 'Bem vindo visitante. \n Data: %s', (date.today()))
    return render(request, 'index.html')

def loguin(request):
    if request.POST:
        # print(' >>>', request.POST)
        formu = forms.autForm(request.POST)
        print(' >>>', formu)
        if formu.is_valid():
            username = formu.cleaned_data.get('nome')
            password = formu.cleaned_data.get('senha')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Loguin feito com sucesso !')
                # separar mensagem para cada user group
                grupo = request.user.groups.all()
                print(grupo)
                if 'caixa' in grupo:
                    if request.user.has_perm('fechar_comanda'):
                        messages.info(request, 'Logado como garçom/caixa. \n Data: %s', (date.today()))
                        return render(request,'feed.html',{'feedpedidos': models.Pedido.objects.all()})
                elif 'cozinha' in grupo:
                    if request.user.has_perm('pedido_pronto'):
                        messages.info(request, 'Logado como cozinha. \n Data: %s', (date.today()))
                        return render(request,'feed.html',{'feedpedidos': models.Pedido.objects.all()})
                elif 'administração' in grupo:
                    messages.info(request, 'Bem vindo administrador. \n Data: %s', (date.today()))
                    if request.user.has_perm('abrir_comanda'):
                        formulario = forms.produto()
                        return render(request,'adm.html',{'form': formulario})
                messages.warning(request, 'cagao')
                print('cagao')
                return redirect('loguin')
            messages.warning(request, 'Dados inválidos')
            return redirect('loguin')
        messages.warning(request, 'Formulrio inválido')
        return render(request, 'loguin.html')
    else:
        print('nao logado')
        return render(request, 'loguin.html',{'form':forms.autForm})


def cardapio(request):
    if request.user.is_authenticated == False:
        messages.info(request, 'Visitante. \n Data: %s', (date.today()))
    else:
        messages.info(request, 'Usuário registrado. \n Data: %s', (date.today()))
    return render(request, 'cardapio.html',{'prod': models.Produtocad.objects.all()})


@login_required(login_url='loguin')
def logoutuser(request):
    logout(request)
    return redirect('index')


@permission_required('ver_feed')
def feed(request):

    return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})


@permission_required('fazer_pedido')
def ped(request):
    if request.POST:
        print(request.POST)
        if 'soucomanda' in request.POST and request.user.has_perm('abrir_comanda'):
            formcom = forms.pedidos(request.POST)
            if formcom.is_valid():
                formcom.save()
    formComanda = forms.comandas
    return render(request, 'pedidos.html',{'newcomanda': formComanda})



# Create your views here.
