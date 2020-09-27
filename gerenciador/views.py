from datetime import date
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password, BCryptPasswordHasher, pbkdf2
from django.contrib.auth import logout, login, authenticate, get_user
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from pprint import pprint
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
                password=formu.cleaned_data.get('senha')
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
        grupo = request.user.groups.all()
        print(grupo)

        if 'caixas' in str(grupo):
            messages.info(request, 'Logado como caixa. \n Data: {}'.format(date.today()))
            return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})  # enviar para as comandas

        elif 'cozinha' in str(grupo):
            if request.user.has_perm('pedido_pronto'):
                messages.info(request, 'Logado como cozinha. \n Data: {}'.format(date.today()))
                return render(request, 'feed.html', {'pedidos': models.Pedido.objects.all()})

        elif 'gerente' in str(grupo):
            return redirect('administrador')

        elif 'garçons' in str(grupo):
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
    estado_mov = models.movi.objects.filter(pk=3).values()
    # fil=models.Pedido.objects.all()[0]['observacao']
    # pprint()

    return render(request, 'feed.html', {

        'pedidos': models.Pedido.objects.all(),
        # breakpoint()
        'movi': estado_mov[0]['movimento']
    })


def ped(request):
    estado_mov = models.movi.objects.filter(pk=3).values()
    if request.POST:
        print(request.POST)


        if 'n_mesa' in request.POST:
            print('kkkkk')
            usr = get_user(request)

            if usr.has_perm('abrir_comanda'):
                formcom = forms.comandas(request.POST)
                print('tem perm')
                if formcom.is_valid():
                    print('foi valido')
                    formcom.save()
                    messages.success(request, "Comanda aberta !")
                    formComanda = forms.comandas
                    return render(request, 'pedidos.html',
                                  {'newcomanda': formComanda,
                                   'prod': models.Produtocad.objects.all(),
                                   'movi':estado_mov[0]['movimento']
                                   })

    else:
        messages.success(request, "{}, Data {}".format(request.user, date.today()))
        formComanda = forms.comandas
        return render(request, 'pedidos.html', {
            'newcomanda': formComanda,
            'prod': models.Produtocad.objects.all(),
            'movi':estado_mov[0]['movimento'],
            'pedido': forms.pedidos

        })


@permission_required('gerenciador.iniciar_movimento')
def adm(request):
    # print('do adm ', request.user.groups.all()[0])
    if request.user.has_perm("gerenciador.iniciar_movimento"):
        if request.POST:
            rq = request.POST
            # useer = forms.mov(rq)

            # print(useer)
            # if useer.is_valid():
            mov_atual = models.movi.objects.all().update(movimento=rq['movimento'])
            # print(mov_atual, 'movaq')
            # print('nudale', rq['movimento'])

            if (mov_atual == 1):
                if (rq['movimento'] == 'L'):

                    messages.info(request, "Movimento iniciado com sucesso !")
                    # print('nudale', rq['movimento'])
                    estado_mov = models.movi.objects.filter(pk=3).values()
                    # print(estado_mov)
                    return render(request, 'adm.html', {'form': forms.produto,
                                                        'prod': models.Produtocad.objects.all(),
                                                        'logado': get_user(request),
                                                        'mov': estado_mov[0]['movimento']
                                                        })

                elif (rq['movimento'] == 'D'):


                    messages.info(request, "Movimento encerrado com sucesso !")
                    # print('trerrekcheck', rq['movimento'])
                    estado_mov = models.movi.objects.filter(pk=3).values()
                    # print(estado_mov)
                    return render(request, 'adm.html', {'form': forms.produto,
                                                        'prod': models.Produtocad.objects.all(),
                                                        'logado': get_user(request),
                                                        'mov': estado_mov[0]['movimento']
                                                        })
            else:
                # messages.error(request, "{}".format('Não foi possível alterar o movimento.'))
                rq = models.movi.objects.filter(pk=3).values()
                return render(request, 'adm.html', {'form': forms.produto,
                                                    'prod': models.Produtocad.objects.all(),
                                                    'logado': get_user(request),
                                                    'mov': rq[0]['movimento']
                                                    })

        else:
            # messages.success(request, "Bem vindo Gerente ! Data {}".format(date.today()))
            # print('grupos ', request.user.groups.all())
            # print(get_user(request))
            rq = models.movi.objects.filter(pk=3).values()
            # estado_mov = models.movi.objects.filter(pk=3)
            # print(rq)
            return render(request, 'adm.html', {'form': forms.produto,
                                                'prod': models.Produtocad.objects.all(),
                                                'logado': get_user(request),
                                                'mov': rq[0]['movimento']
                                                })
    else:
        messages.danger(request, "Você não tem permissão para acessar esta página.")
        return redirect('index')
# Create your views here.
