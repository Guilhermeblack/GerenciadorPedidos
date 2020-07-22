from datetime import date
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password, BCryptPasswordHasher, pbkdf2
from django.contrib.auth import logout, login, authenticate, get_user
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission

from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from Atendgb import settings
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
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)

            messages.error(request, 'Dados inválidos')
            return render(request, 'loguin.html', {'form': forms.autForm})
        messages.error(request, 'Formulrio inválido')
        return render(request, 'loguin.html', {'form': forms.autForm})
    else:
        if request.user.is_authenticated:
            return redirect('profile')

        return render(request, 'loguin.html', {'form': forms.autForm})


def profile(request):

    if request.user.is_authenticated:
        usr = get_user(request)
        grupo = request.user.groups.all()[0]


        if 'caixas' == str(grupo):
            messages.info(request, 'Logado como caixa. \n Data: {}'.format(date.today()))
            return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})  # enviar para as comandas

        elif 'cozinha' == str(grupo):
            if request.user.has_perm('pedido_pronto'):
                messages.info(request, 'Logado como cozinha. \n Data: {}'.format(date.today()))
                return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})

        elif 'gerente' == str(grupo):
            return redirect('administrador')

        elif 'garçons' == str(grupo):
            messages.info(request, 'Bem vindo Garçom. \n Data: {}'.format(date.today()))
            formComanda = forms.comandas
            return render(request, 'pedidos.html',
                            {'newcomanda': formComanda, 'produtos': models.Produtocad.objects.all()})
        else:
            messages.info(request, 'Usuário nao identificado. \n Data: {}'.format(date.today()))
            # return redirect('loguin')

        print(request, "erro nos grupos")
    return redirect('index')


@login_required(login_url='loguin')
def logoutuser(request):
    logout(request)
    return redirect('index')


# @permission_required('ver_feed')
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
        messages.success(request, "{}, Data {}".format(request.user, date.today()))
        formComanda = forms.comandas
        return render(request, 'pedidos.html', {'newcomanda': formComanda, 'prod': models.Produtocad.objects.all()})


@permission_required('gerenciador.iniciar_movimento')
def adm(request):

    # print('do adm ', request.user.groups.all()[0])
    if request.user.has_perm("gerenciador.iniciar_movimento"):
        if request.POST:
            rq = request.POST
            print(rq)
            breakpoint()
            user = forms.mov(request.POST)
            if user.is_valid():
                ger = get_user(request)
                env = models.Gerente.objects.all(user=ger)
                env=user
                env.save()
                if(user.cleaned_data('movimento') == 'L'):
                    messages.alert(request, "{}".format('Movimento iniciado com sucesso'))
                elif(user.cleaned_data('movimento') == 'D'):
                    messages.alert(request, "{}".format('Movimento encerrado com sucesso'))
        else:
            messages.success(request, "Bem vindo Gerente ! Data {}".format(date.today()))
            # print('grupos ', request.user.groups.all())
            print(get_user(request))
            return render(request, 'adm.html', {'form': forms.produto,
                                                'prod': models.Produtocad.objects.all(),
                                                'logado': get_user(request)
                                                })
    else:
        messages.danger(request, "Você não tem permissão para acessar esta página.")
        return redirect('index')
# Create your views here.
