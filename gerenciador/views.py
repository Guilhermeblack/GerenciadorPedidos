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
                if 'garçom' or 'caixa' in grupo:
                    messages.info(request, 'Logado como garçom/caixa. \n Data: %s', (date.today()))
                    return redirect('ped')
                elif 'cozinha' in grupo:
                    messages.info(request, 'Logado como cozinha. \n Data: %s', (date.today()))
                    return redirect('feed')
                elif 'administração' in grupo:
                    messages.info(request, 'Bem vindo administrador. \n Data: %s', (date.today()))
                    permission_required('controlar_produtos')
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
    return render(request, 'cardapio.html',{'prod': models.Produto.objects.all()})


@login_required()
def logoutuser(request):
    logout(request)
    return redirect('index')


@login_required()
@permission_required('ver_feed')
def feed(request):

    return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})

@login_required()
@permission_required('fazer_pedido')
def ped(request):
    # status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    return render(request, 'pedidos.html')



# Create your views here.
