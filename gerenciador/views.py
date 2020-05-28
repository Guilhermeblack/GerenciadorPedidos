from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect


from . import models, forms


def index(request):
    if request.user.is_authenticated == False:
        messages.info(request, 'Bem vindo visitante.  \n Data: {}'.format(date.today()))
    else:
        messages.info(request, 'Bem vindo {}.  \n Data: {}'.format(request.user, date.today()))
    return render(request, 'index.html')

@csrf_protect
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
                grupo = request.user.groups.all()[0]
                print(grupo)
                if 'caixas' == grupo:
                        messages.info(request, 'Logado como caixa. \n Data: {}'.format(date.today()))
                        return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()}) # enviar para as comandas

                elif 'cozinha' == grupo:
                        messages.info(request, 'Logado como cozinha. \n Data: {}'.format(date.today()))
                        return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})

                elif 'gerente' == grupo:
                    messages.info(request, 'Bem vindo gerente. \n Data: {}'.format(date.today()))
                    formulario = models.Produtocad.objects.all()
                    return redirect(adm)

                elif 'garçons' == str(grupo):
                    messages.info(request, 'Bem vindo garçom. \n Data: {}'.format(date.today()))
                    formComanda = forms.comandas
                    return render(request, 'pedidos.html',{'newcomanda': formComanda, 'produtos': models.Produtocad.objects.all()})

            # depois de logar ele continua na view/url de loguin,
            #entao onde ele for pede loguin/algo
            #sair daqui depois de logar


            messages.error(request, 'Dados inválidos')
            return redirect('loguin')
        messages.error(request, 'Formulrio inválido')
        return render(request, 'loguin.html')
    else:
        return render(request, 'loguin.html',{'form': forms.autForm})


def cardapio(request):
    if request.user.is_authenticated == False:
        messages.info(request, 'Visitante. \n Data: {}'.format(date.today()))

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
            print('tem perm')
            if formcom.is_valid():
                print('foi valido')
                formcom.save()
                messages.success(request, "pedido feito com sucesso !")
    formComanda = forms.comandas
    return render(request, 'pedidos.html',{'newcomanda': formComanda, 'produtos': models.Produtocad.objects.all()})

def adm(request):
    if authenticate(request.user):
        formulario = forms.produto
        return render(request, 'adm.html', {'form': formulario})


# Create your views here.
