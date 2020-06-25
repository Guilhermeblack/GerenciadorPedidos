from datetime import date
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password, BCryptPasswordHasher, pbkdf2
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect
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
        # print(' >>>', formu)
        if formu.is_valid():
            username = formu.cleaned_data.get('nome')
            # password = make_password(formu.cleaned_data.get('senha'), salt=None, hasher='pbkdf2_sha256')
            # print(password)
            user = authenticate(
                username=username,
                password= formu.cleaned_data.get('senha')
            )

            if user is not None:
                login(request, user)
                messages.success(request, 'Loguin feito com sucesso !')
                # separar mensagem para cada user group
                grupo = request.user.groups.all()[0]
                print(grupo)
                if 'caixas' == str(grupo):
                    messages.info(request, 'Logado como caixa. \n Data: {}'.format(date.today()))
                    return redirect(request,'feed.html',{'pedidos': models.Pedido.objects.all()})  # enviar para as comandas

                elif 'cozinha' == str(grupo):
                    if request.user.has_perm('pedido_pronto'):
                        messages.info(request, 'Logado como cozinha. \n Data: {}'.format(date.today()))
                        return redirect(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})

                elif 'gerente' == str(grupo):
                    messages.info(request, 'Bem vindo Gerente. \n Data: {}'.format(date.today()))
                    formulario = models.Produtocad.objects.all()
                    # precisa sair daqui para a view de adm
                    return redirect('administrador')

                elif 'garçons' == str(grupo):
                    messages.info(request, 'Bem vindo garçom. \n Data: {}'.format(date.today()))
                    formComanda = forms.comandas
                    return redirect(request, 'pedidos.html',
                                  {'newcomanda': formComanda, 'produtos': models.Produtocad.objects.all()})

                # depois de logar ele continua na view/url de loguin,
                # entao onde ele for pede loguin/algo
                # sair daqui depois de logar

                messages.error(request, "erro nos grupos")
                print('cagao')
                # return redirect('loguin')
            messages.error(request, 'Dados inválidos')
            # return redirect('loguin')
        messages.error(request, 'Formulrio inválido')
        # return render(request, 'loguin.html')
    else:
        return render(request, 'loguin.html', {'form': forms.autForm})


@login_required(login_url='loguin')
def logoutuser(request):
    logout(request)
    return redirect('index')


@permission_required('ver_feed')
def feed(request):
    return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})


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
    else:
        messages.success(request, "{}, Data {}".format('usuario', date.today()))
        formComanda = forms.comandas
        return render(request, 'pedidos.html', {'newcomanda': formComanda, 'prod': models.Produtocad.objects.all()})


@permission_required('iniciar_movimento')
def adm(request):
    if request.POST:
        rq = request.POST
        print(rq)
    messages.success(request, "Bem vindo Gerente ! Data {}".format(date.today()))
    return render(request, 'adm.html', {'form': forms.produto, 'prod': models.Produtocad.objects.all()})

# Create your views here.
