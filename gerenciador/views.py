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
    estado_mov = models.movi.objects.filter(pk=1).values()
    STATUS_CHOICES = (
        "Pedido realizado",
        "Fazendo",
        "Saiu para entrega",
        "Foi entregue",
        "Cancelado"
    )

    if request.POST:
        # print(request.POST)

        if 'exc_ped' in request.POST:
            # pprint(request.POST)
            ped = models.Pedido.objects.filter(pk=request.POST['exc_ped'])
            ped.update(status="C")
            # pprint(ped[0].comandaref.id)
            produto_ped = models.Produtocad.objects.filter(pk=ped[0].produtosPed.all()[0].id)

            comanda = models.Comanda.objects.filter(pk=ped[0].comandaref.id)

            vlr = comanda[0].valor - (ped[0 ].quantidade *produto_ped[0].preco)
            pprint(vlr)
            comanda.update(valor=vlr)
            messages.success(request, "{}, Pedido cancelado com sucesso!".format(request.user))
            return render(request, 'feed.html', {

                'comandas': models.Comanda.objects.all().order_by('id', 'data'),
                'pedidos': models.Pedido.objects.all().order_by('id', 'status'),
                'choices': STATUS_CHOICES,
                'movi': estado_mov[0]['movimento']
            })

        if 'stats' in request.POST:
            print(request.POST)
            ped= models.Pedido.objects.filter(pk=request.POST['idstat'])
            pprint(ped)
            ped.update(status=request.POST['stats'])
            # ped.save()
            messages.success(request, "{}, status alterado com sucesso.".format(request.user))
            return render(request, 'feed.html', {

                'comandas': models.Comanda.objects.all().order_by('id', 'data'),
                'pedidos': models.Pedido.objects.all().order_by('id', 'status'),
                'choices': STATUS_CHOICES,
                'movi': estado_mov[0]['movimento']
            })

        if 'comanda_x' in request.POST:
            # tirar do total da comanda
            com = models.Comanda.objects.filter(pk=request.POST['comanda_x'])[0]
            valo_ped = float(request.POST['valo'])
            peed = request.POST['pedi[]']

            com.valor -= valo_ped
            if com.valor <= 0:
                com.status = "F"
                messages.success(request, "{}, Comanda FECHADA com sucesso.".format(request.user))
            else:

                # loop itens
                valo= valo_ped
                if peed.isdigit:
                    pedido_prod = models.Pedido.objects.filter(pk=peed)
                    pprint(pedido_prod[0].produtosPed.all()[0].preco)
                    if valo >= pedido_prod[0].produtosPed.all()[0].preco:

                        valo -= pedido_prod[0].produtosPed.all()[0].preco
                        pedido_prod[0].status_pago = "P"
                    else:
                        if valo > 0:
                            pdt = models.Produtocad.objects.filter(pk=peed)
                            res = pdt.preco - valo
                            com.valor += res
                            pedido_prod[0].status_pago = "R"

                elif peed.length > 1:
                    for num, p in peed:

                        pedido_prod = models.Pedido.objects.filter(pk=p)
                        if valo >= pedido_prod[0].produtosPed.all()[0].preco:

                            valo -= pedido_prod[0].produtosPed.all()[0].preco
                            pedido_prod.status_pago = "P"
                        else:
                            if valo > 0:
                                pdt = models.Produtocad.objects.filter(pk=pedido_prod.produtosPed.all()[0].id)
                                res = pdt.preco - valo
                                com.valor += res
                                pedido_prod.status_pago = "R"

                    messages.success(request, "{}, Comanda ATUALIZADA com sucesso.".format(request.user))

            return render(request, 'feed.html', {

                'comandas': models.Comanda.objects.all().order_by('id', 'data'),
                'pedidos': models.Pedido.objects.all().order_by('id', 'status'),
                'choices': STATUS_CHOICES,
                'movi': estado_mov[0]['movimento']
            })

    else:
        messages.success(request, "{}, Data {}".format(request.user, date.today()))

        # pprint(models.Pedido.objects.all().order_by('id'))
        return render(request, 'feed.html', {

            'comandas': models.Comanda.objects.all().order_by('id', 'data'),
            'pedidos': models.Pedido.objects.all().order_by('id'),
            'choices': STATUS_CHOICES,
            'movi': estado_mov[0]['movimento']
        })


def ped(request):
    estado_mov = models.movi.objects.filter(pk=1).values()
    formComanda = forms.comandas
    if request.POST:
        # print(request.POST)


        if 'n_mesa' in request.POST:
            usr = get_user(request)

            pprint(request.POST)

            # if usr.has_perm('abrir_comanda'):
            formcom = forms.comandas(request.POST)

            pprint(formcom)

            # criar verificação do numero da comanda se nao esta aberta para nao repetir numero

            # print('tem perm')
            if formcom.is_valid():
                formcom.save()
                messages.success(request, "Comanda aberta !")
                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.all(),
                               'movi':estado_mov[0]['movimento'],
                               'comandas': models.Comanda.objects.filter(status="A"),
                               'pedido': forms.pedidos
                               })
            else:
                messages.warning(request, "Formulário inválido!")

                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.all(),
                               'movi': estado_mov[0]['movimento'],
                               'comandas': models.Comanda.objects.filter(status="A"),
                               'pedido': forms.pedidos
                               })

        if 'comandaref' in request.POST:
            # produto = models.Produtocad.objects.get(pk=request.POST['produtosPed'])
            newped = forms.pedidos(request.POST)

            # jogar campo por campo e jogar o produto depois

            if newped.is_valid():
                newped.save()
                add_comanda = models.Comanda.objects.get(pk=request.POST['comandaref'])
                prod = models.Produtocad.objects.get(pk=request.POST['produtosPed'])

                qnt = int(request.POST['quantidade'])
                add_comanda.valor += (prod.preco* qnt)
                add_comanda.save()
                messages.success(request, "Pedido registrado !")
                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.all(),
                               'movi': estado_mov[0]['movimento'],
                               'comandas': models.Comanda.objects.filter(status="A"),
                               'pedido': forms.pedidos
                               })
            else:
                messages.warning(request, "Dados de registro inválidos !")

                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.all(),
                               'movi': estado_mov[0]['movimento'],
                               'comandas': models.Comanda.objects.filter(status="A"),
                               'pedido': forms.pedidos
                               })


    else:
        messages.success(request, "{}, Data {}".format(request.user, date.today()))
        return render(request, 'pedidos.html', {
            'newcomanda': formComanda,
            'prod': models.Produtocad.objects.all(),
            'comandas': models.Comanda.objects.filter(status= "A"),
            'movi':estado_mov[0]['movimento'],
            'pedido': forms.pedidos()

        })


@permission_required('gerenciador.iniciar_movimento')
def adm(request):
    # print('do adm ', request.user.groups.all()[0])
    if request.user.has_perm("gerenciador.iniciar_movimento"):
        rq = request.POST
        if request.POST:

            pprint(rq)
            # if 'prod_x' in rq:

            if 'prod_x' in rq:

                models.Produtocad.objects.filter(pk=request.POST['prod_x']).delete()
                estado_mov = models.movi.objects.filter(pk=1).values()
                messages.info(request, "Produto deletado com sucesso!")
                return render(request, 'adm.html', {'form': forms.produto,
                                                    'prod': models.Produtocad.objects.all(),
                                                    'logado': get_user(request),
                                                    'mov': estado_mov[0]['movimento']
                                                    })

            if 'movimento' in rq:
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
                        estado_mov = models.movi.objects.filter(pk=1).values()
                        # print(estado_mov)
                        return render(request, 'adm.html', {'form': forms.produto,
                                                            'prod': models.Produtocad.objects.all(),
                                                            'logado': get_user(request),
                                                            'mov': estado_mov[0]['movimento']
                                                            })

                    elif (rq['movimento'] == 'D'):


                        messages.info(request, "Movimento encerrado com sucesso !")
                        # print('trerrekcheck', rq['movimento'])
                        estado_mov = models.movi.objects.filter(pk=1).values()
                        # print(estado_mov)
                        return render(request, 'adm.html', {'form': forms.produto,
                                                            'prod': models.Produtocad.objects.all(),
                                                            'logado': get_user(request),
                                                            'mov': estado_mov[0]['movimento']
                                                            })
                else:
                    # messages.error(request, "{}".format('Não foi possível alterar o movimento.'))
                    rq = models.movi.objects.filter(pk=1).values()
                    return render(request, 'adm.html', {'form': forms.produto,
                                                        'prod': models.Produtocad.objects.all(),
                                                        'logado': get_user(request),
                                                        'mov': rq[0]['movimento']
                                                        })
            if 'tipo' in rq:
                new_prod = forms.produto(rq)
                if new_prod.is_valid():
                    new_prod.save()
                    messages.success(request, "Produto cadastrado !")
                    return redirect('administrador')
                else:
                    messages.warning(request, "Dados inválidos !")
        else:
            if 'pesq_prod' in request.GET:
                pprint(request.GET)


            rq = models.movi.objects.filter(pk=1).values()
            # estado_mov = models.movi.objects.filter(pk=1)
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
