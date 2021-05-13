from datetime import date
import datetime

import cloudinary
import django_pagarme
import base64
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password, BCryptPasswordHasher, pbkdf2
from django.contrib.auth import logout, login, authenticate, get_user
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission, User, Group
from pprint import pprint
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import django.db.models.signals
from Atendgb import settings
from . import models, forms


def index(request):
    if request.user.is_authenticated == False:
        messages.info(request, 'Bem vindo visitante.  \n Data: {}'.format(date.today()))
    else:
        messages.info(request, 'Bem vindo {}.  \n Data: {}'.format(request.user, date.today()))
    return render(request, 'index.html')


def sobre(request):
    return render(request, 'sobre.html', {
        'user': request.user,
    })  # enviar para as comandas


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
            return render(request, 'loguin.html', {
                #trazer os usuarios dessa loja
                'form': forms.autForm
            })
        messages.error(request, 'Formulrio inválido')
        return render(request, 'loguin.html', {
            # trazer os usuarios dessa loja
            'form': forms.autForm

        })
    else:

        if request.user.is_authenticated and request.user.has_perm("gerenciador.iniciar_movimento") :

            nc = models.Newcli.objects.get(user=request.user)
            if nc:
                loja = nc.loja
            else:
                loja = ''

            nl = models.Newcli.objects.filter(loja = loja)
            if request.user.has_perm('iniciar_movimento'):
                return render(request, 'loguin.html', {
                    # trazer os usuarios dessa loja
                    'cad': nl,
                    'form': forms.autForm

                })
            return redirect('profile')

        return render(request, 'loguin.html', {'form': forms.autForm})

@csrf_protect
def new(request):

    # if request.user.is_authenticated
    if request.POST:
        pprint(request.POST)
        gp = Group.objects.get(name=request.POST['groupocli'])
        print(' --- ')
        pprint(gp)
        print('post da loja')

        #cria loja

        lj = forms.Newloja(request.POST )
        # pprint(lj)
        if lj.is_valid():
            lojinha = lj.save()
        else:
            nl = models.Newcli.objects.get(user=request.user)
            lojinha = nl.loja
        gr = request.POST

        ger = forms.Newcli(gr )

        pprint(ger)
        if ger.is_valid():
            print('bateeu')


            pprint(lojinha)
            gerente = ger.save(commit= False)
            gerente.loja = lojinha
        # gerente.save(commit= False)
            print(' nodaleee ')
            gerente.loja = lojinha
            gerente.save()
            gerente.groups.add(gp)

            pprint(gerente)
            cli = models.Newcli.objects.create(user=gerente, loja=lojinha)
            cli.save()

            gp.save()
            s = authenticate(
                username=gerente.username,
                password=gerente.password
            )

            if s is not None:
                print('loho fdp')
                login(request, s)

                messages.info(request, 'Parabens, sua loja foi aberta. \n --  {}'.format(date.today()))
                return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)
            # user = User.objects.create_user(request.POST['Usuario'], request.POST['Email'], request.POST['Senha'] )
            # user.first_name = request.POST['Nome']
            # user.last_name = request.POST['Sobrenome']
            # user.has_perm('gerente.add_bar')
            # user.permissions.set(['fazer_pedido', 'ver_feed','iniciar_movimento','fechar_comanda','abrir_comanda','controlar_produtos'])
            #
            # user.groups.add(gp)
            # user.save()

            # pprint(gerente)
    return render(request, 'newcliente.html',{
        'loja': forms.Newloja,
        'clie': forms.Newcli,
        'groups': Group.objects.all()
    })


def profile(request):


    if not models.Newcli.objects.all():
        print('tentei')
        nt = models.Newcli.objects.create(user=request.user)
        nt.save()
    if request.user.is_authenticated:

        nc = models.Newcli.objects.get(user=request.user)
        if nc:
            loja = nc.loja
        else:
            loja = ''
        usr = get_user(request)
        grupo = request.user.groups.all()
        # print(grupo)

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
    nc = models.Newcli.objects.get(user=request.user)
    loja = nc.loja

    pprint(loja)
    estado_mov = loja.movimento
    STATUS_CHOICES = (
        "Pedido realizado",
        "Fazendo",
        "Saiu para entrega",
        "Foi entregue",
        "Cancelado"
    )
    FORMA_PGT = (
        "Cartão",
        # "Pix",
        "Dinheiro"
    )
    if request.POST:
        # print(request.POST)

        if 'exc_ped' in request.POST:
            pprint(request.POST)
            ped = models.Pedido.objects.get(pk=request.POST['exc_ped'], loja=loja)
            ped.status="C"
            ped.valor =0
            # pprint(ped)
            pprint(ped.produtosPed.all())
            produto_ped = models.Produtocad.objects.get(pk=ped.produtosPed.all()[0].id,loja=loja)

            comanda = models.Comanda.objects.get(pk=ped.comandaref.id,loja=loja)
            vll = ped.quantidade *produto_ped.preco
            print(vll, '  <<< vll')
            # comanda.valor -= vll

            # em caso de pedido cancelado eu retorno as quantidades de insumo ao estoque
            pega_prod = models.Insumos.objects.filter(produto_prod=produto_ped.id, loja=loja)
            for ins in pega_prod:
                pprint(ins.insumo_prod)
                ins.insumo_prod.quantidade = ins.insumo_prod.quantidade + ins.quantidade_prod
                ins.insumo_prod.save()

            comanda.save()
            ped.save()
            # o produto recebe de volta sua quantidade de acorco com pedido


            # os Insumos recebem de volta sua quantidade conforme o que é usado no produto vezes quantidade do produto
            messages.success(request, "{}, Pedido cancelado com sucesso!".format(request.user))
            return render(request, 'feed.html', {

                'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
                'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id', 'status'),
                'choices': STATUS_CHOICES,
                'fpg': FORMA_PGT,
                'movi': estado_mov
            })

        if 'stats' in request.POST:
            print(request.POST)
            ped= models.Pedido.objects.get(pk=request.POST['idstat'],loja=loja)
            pprint(ped)
            ped.update(status=request.POST['stats'])
            # ped.save()
            messages.success(request, "{}, status alterado com sucesso.".format(request.user))
            return render(request, 'feed.html', {

                'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
                'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id', 'status'),
                'choices': STATUS_CHOICES,
                'fpg': FORMA_PGT,
                'movi': estado_mov
            })

        if 'comanda_x' in request.POST:
            # tirar do total da comanda

            pprint(request.POST)

            com = models.Comanda.objects.get(pk=int(request.POST['comanda_x']),loja=loja)
            valo_ped = float(request.POST['valo'])

            # loop itens

            valo= valo_ped
            if 'pedi[]' in request.POST:
                peed = request.POST['pedi[]']
                pprint(peed)
                print('entao foi o pedd')

                if isinstance(peed, str):
                    pedido_prod = models.Pedido.objects.get(pk=peed, loja=loja)
                    print('apenas um item sendo pago')
                    com.valor -= valo_ped
                    if valo >= pedido_prod.valor:
                        if com.valor <= 0:
                            com.status = "F"
                            receb = models.Pagamentos.objects.create(
                                valor=float(valo_ped),
                                status="F",
                                loja= loja
                            )

                            receb.pedidored.add(pedido_prod)

                            receb.save()
                            com.save()
                            new_status = 'FECHADA'
                            print('valor comanda menor q 0')
                        valo -= pedido_prod.valor
                        print('valor paga o produto unico do pedido')
                        pedido_prod.valor = 0
                        pedido_prod.status_pago = "P"
                        receb = models.Pagamentos.objects.create(
                            valor=valo_ped,
                            status= "P",
                            loja=request.user.loja
                        )
                        receb.pedidored.add(pedido_prod)
                        receb.save()
                        com.save()
                        pedido_prod.save()

                    else:

                        if valo > 0:
                            print('valor nao paga produto sobra {} ')
                            print(valo,'  valoo')
                            pedido_prod.valor -= valo
                            print(com.valor,'  comanda valoor')
                            print(pedido_prod.valor,'  valor do pedido')
                            pedido_prod.status_pago = "R"
                            receb = models.Pagamentos.objects.create(
                                valor=valo_ped,
                                status="R",
                                loja=request.user.loja
                            )
                            receb.pedidored.add(pedido_prod)
                            receb.save()
                            pedido_prod.save()
                            com.save()
                            print('passo aqui')
                    pedido_prod.save()
                    new_status = 'ATUALIZADA com sucesso'


                elif peed.length > 0:
                    pprint('mais de um produto no pedido')
                    com.valor -= valo_ped
                    for num, p in peed:
                        pprint('loop dos produtos sendo pagos')
                        pprint(p)
                        pedido_prod = models.Pedido.objects.get(pk=p)

                        if valo >= pedido_prod.produtosPed.all()[0].preco:
                            print('valor sendo pago {}  é maior que valor do produto {}'.format(valo,pedido_prod.produtosPed.all()[0].preco ))
                            valo -= pedido_prod.produtosPed.all()[0].preco * pedido_prod.produtosPed.all()[0].quantidade
                            pedido_prod.valor -= valo
                            pedido_prod.status_pago = "P"
                            receb = models.Pagamentos.objects.create(
                                valor=valo_ped,
                                status="P",
                                loja=request.user.loja
                            )
                            receb.pedidored.add(pedido_prod)
                            receb.save()
                            pedido_prod.save()
                        else:
                            print('valor do produto pagou o valor do pedido aqui'.format(valo))
                            if valo > 0:
                                print('valor do pagamento nao pagou produto mas tem restante >>>')
                                pdt = models.Produtocad.objects.get(pk=pedido_prod.produtosPed.all()[0].id, loja=loja)
                                pprint(pdt)
                                res = pdt.preco - valo
                                com.valor += res
                                pedido_prod.valor = res
                                pedido_prod.status_pago = "R"
                                receb = models.Pagamentos.objects.create(
                                    valor=valo_ped,
                                    status="R",
                                    loja=request.user.loja
                                )
                                receb.pedidored.add(pedido_prod)
                                receb.save()
                                pedido_prod.save()
                            elif valo <= 0:


                                print('fecho o valor do pedido {}'.format(valo))
                                com.save()
                    new_status = 'ATUALIZADA com sucesso'
                    pedido_prod.save()
                    com.save()

                if com.valor <= 0:

                    com.status="F"
                    if com.valor <= 0:
                        com.status = "F"
                        receb = models.Pagamentos.objects.create(
                            valor=valo_ped,
                            status="F",
                            loja=request.user.loja
                        )
                        receb.pedidored.add(pedido_prod)
                        receb.save()
                        com.save()
                        new_status = 'FECHADA'
                    com.save()
                    new_status = 'FECHADA'
            else:
                new_status = 'Sem pedido Selecionado'


            messages.success(request, "{}, Comanda {} .".format(request.user, new_status))


            return render(request, 'feed.html', {

                'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
                'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id', 'status'),
                'choices': STATUS_CHOICES,
                'fpg': FORMA_PGT,
                'movi': estado_mov
            })

    else:
        messages.success(request, "{}, Data {}".format(request.user, date.today()))

        # pprint(models.Pedido.objects.all().order_by('id'))
        return render(request, 'feed.html', {

            'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
            'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id'),
            'choices': STATUS_CHOICES,
            'fpg': FORMA_PGT,
            'movi': estado_mov
        })


def ped(request):


    if request.user.is_authenticated:
        nc = models.Newcli.objects.get(user=request.user)
        pprint(nc.loja)
        loja = nc.loja
        if 'gerente' == request.user.groups:
            messages.warning(
                request,
                " caiu logadin {}".format(request.user)
            )
    pprint(loja)
    estado_mov = loja.movimento
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
                formco = formcom.save(commit=False)
                formco.loja = loja
                password = ""+request.POST['nome']+request.POST['n_mesa']+""
                user_comanda = models.User.objects.create_user(
                    username=request.POST['nome'],
                    password=password,
                    email= request.POST['nome']+"@mail.com"
                )
                user_comanda.groups.add(Group.objects.get(name='cliente'))
                user_comanda.save()
                clientec = models.Newcli.objects.create(
                    user = user_comanda,
                    loja = loja

                )
                clientec.save()

                formco.save()
                messages.success(request, "Comanda aberta !")
                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.filter(loja=loja),
                               'movi':estado_mov,
                               'comandas': models.Comanda.objects.filter(status="A",loja=loja),
                               'pedido': forms.pedidos
                               })
            else:
                messages.warning(request, "Formulário inválido!")

                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.filter(loja=loja),
                               'movi': estado_mov,
                               'comandas': models.Comanda.objects.filter(status="A",loja=loja),
                               'pedido': forms.pedidos
                               })

        if 'comandaref' in request.POST:

            # pprint(request.POST)
            newped = forms.pedidos(request.POST)
            pprint(request.user.groups.all())
            print('printou o grupo')
            # jogar campo por campo e jogar o produto depois

            if newped.is_valid():
                messag =''
                add_comanda = models.Comanda.objects.get(pk=request.POST['comandaref'],loja=loja)
                prod = models.Produtocad.objects.get(pk=request.POST['produtosPed'],loja=loja)

                qnt = int(request.POST['quantidade'])
                # print(newped)
                #verifico se o produto tem a quantidade para poder ser feito pedido
                if prod.quantidade:
                    if prod.quantidade > 0:
                        prod.quantidade = prod.quantidade - 1
                        if prod.quantidade < prod.qnt_minima and  request.user.groups.all()[0].name == 'gerente':
                            messag = " Quantidade mínima do(a) {} atingido. Reabasteça o estoque".format(prod.nome)
                            messages.warning(request, messag)
                    else:
                        messag = " Estoque do(a) {} insuficiente. Reabasteça o estoque".format(prod.nome)
                        messages.warning(request, messag)
                        prod.cardapio = False
                        prod.save()

                valu = prod.preco * qnt
                newped.cleaned_data['valor'] =float(valu)
                newped['valor'].value = valu
                print(newped.cleaned_data, '  <<<')
                if newped.is_valid():
                    j = newped.save(commit=False)
                    j.loja = loja
                    j.save()

                    pega_prod = models.Insumos.objects.filter(produto_prod= prod.id,loja=loja)[0]
                    # result.filter(tipo__in=rq['cat_comanda'])
                    pprint(pega_prod)
                    for ins in pega_prod:
                        # verifico se o insumo tem a quantidade para poder ser feito pedido
                        if ins.insumo_prod.quantidade > 0:
                            print(ins.quantidade_prod, ' - quantidade a tirar')
                            print(ins.insumo_prod.quantidade,' - quantidade produto')
                            ins.insumo_prod.quantidade = ins.insumo_prod.quantidade - ins.quantidade_prod
                            if ins.insumo_prod.quantidade < ins.insumo_prod.qnt_minima and request.user.groups.all()[0].name == 'gerente':
                                print('pedou um negativo')
                                messag =  " Quantidade mínima do(a) {} atingido. Reabasteça o estoque".format(prod.nome)
                                messages.warning(request, messag)
                            sv = ins.insumo_prod.save()
                            print(ins.insumo_prod.quantidade ,' total')
                        else:
                            messag = " Estoque do(a) {} insuficiente. Reabasteça o estoque".format(prod.nome)
                            messages.warning(request, messag)
                            ins.insumo_prod = False
                            ins.insumo_prod.save()
                            prod.cardapio = False
                            prod.save()
                    # esse for fez a retirada da quantidade dos insumos
                    j.save()
                    # aqui salvou o pedido

                    #subtrair dos produtos a quantidade que foi no pedido pra cada insumo
                    #a quantidade total é o é usado no produto vezes produtos pedidos
                    ped_val = models.Pedido.objects.filter(pk=j.id,loja=loja)[0]
                    # print(ped_val.valor, '  valor q fico d opedido')
                    ped_val.valor= valu
                    # print(ped_val.valor, '  depois e salv')
                    ped_val.save()


                    # print(newped.cleaned_data['valor'])
                add_comanda.valor += valu
                add_comanda.save()
                messag = "  Pedido registrado !"
                print(messag)
                messages.success(request, messag)

                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.filter(loja=loja),
                               'movi': estado_mov,
                               'comandas': models.Comanda.objects.filter(status="A",loja=loja),
                               'pedido': forms.pedidos
                               })
            else:
                messages.warning(request, "Dados de registro inválidos !")

                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.filter(loja=loja),
                               'movi': estado_mov,
                               'comandas': models.Comanda.objects.filter(status="A",loja=loja),
                               'pedido': forms.pedidos
                               })
        messages.warning(request, "Ação inválida !")
        return redirect('pedidos')
    else:
        messages.success(request, "{}, Data {}".format(request.user, date.today()))
        return render(request, 'pedidos.html', {
            'newcomanda': formComanda,
            'prod': models.Produtocad.objects.filter(loja=loja),
            'comandas': models.Comanda.objects.filter(status= "A",loja=loja),
            'movi':estado_mov,
            'pedido': forms.pedidos()

        })


@permission_required('gerenciador.iniciar_movimento')
def adm(request):
    # print('do adm ', request.user.groups.all()[0])

    nc = models.Newcli.objects.get(user=request.user)
    loja = nc.loja
    if request.user.has_perm("gerenciador.iniciar_movimento"):

        if request.POST:
            rq = request.POST
            pprint(rq)
            # if 'prod_x' in rq:
            #deleta um produto
            if 'prod_x' in rq:

                models.Produtocad.objects.filter(pk=request.POST['prod_x'],loja=loja).delete()
                estado_mov = loja.movimento
                messages.info(request, "Produto deletado com sucesso!")
                return render(request, 'adm.html', {'form': forms.produto,
                                                    'prod': models.Produtocad.objects.get(loja=loja),
                                                    'logado': get_user(request),
                                                    'mov': estado_mov
                                                    })
            #altera o movimento
            if 'movimento' in rq:
                # useer = forms.mov(rq)

                # print(useer)
                # if useer.is_valid():
                # mov_atual = models.Loja.objects.all().update(movimento=rq['movimento'], loja=loja)
                # print(mov_atual, 'movaq')
                # print('nudale', rq['movimento'])

                if loja:
                    if rq['movimento'] == 'L':

                        messages.info(request, "Movimento iniciado com sucesso !")
                        # print('nudale', rq['movimento'])
                        loja.movimento = "L"
                        loja.save()
                        estado_mov = loja.movimento
                        # print(estado_mov)
                        return render(request, 'adm.html', {'form': forms.produto,
                                                            'prod': models.Produtocad.objects.filter(loja=loja),
                                                            'logado': get_user(request),
                                                            'mov': estado_mov
                                                            })

                    elif rq['movimento'] == 'D':

                        loja.movimento = "D"
                        loja.save()
                        messages.info(request, "Movimento encerrado com sucesso !")
                        # print('trerrekcheck', rq['movimento'])
                        estado_mov = loja.movimento
                        # print(estado_mov)
                        return render(request, 'adm.html', {'form': forms.produto,
                                                            'prod': models.Produtocad.objects.filter(loja=loja),
                                                            'logado': get_user(request),
                                                            'mov': estado_mov
                                                            })
                else:
                    # messages.error(request, "{}".format('Não foi possível alterar o movimento.'))
                    rq = loja.movimento
                    return render(request, 'adm.html', {'form': forms.produto,
                                                        'prod': models.Produtocad.objects.filter(loja=loja),
                                                        'logado': get_user(request),
                                                        'mov': rq
                                                        })
            if 'tipo' in rq:
                if 'img_prod' in request.FILES:
                    rf= request.FILES
                nprod = rq
                # Insumos = rq['qnt_ins[]']
                # pprint(nprod)
                cont=[]
                nprod._mutable = True
                for p in list(rq):
                    if p.isnumeric():
                        # print('enumero')
                        epc = float(rq[p].replace(',', '.'))
                        print(epc)

                        print(p)
                        ins = models.Insumos.objects.create(
                            quantidade_prod=epc,
                            insumo_prod=models.Produtocad.objects.get(pk= p,loja=loja),
                            loja=request.user.loja

                        )
                        ins.save()
                        cont.append(ins.id)
                        nprod.pop(p)
                # breakpoint(rq)
                if 'cardapio' not in nprod:
                    nprod['cardapio'] = False
                if(nprod['cardapio'] == 'on'):
                    nprod['cardapio'] = True
                else:
                    nprod['cardapio'] = False
                nprod._mutable = False
                new_prod = forms.produto(nprod, rf)
                pprint(new_prod)

                print(new_prod.errors)
                if new_prod.is_valid():

                    new_pro =new_prod.save(commit=False)

                    new_pro.loja = loja
                    # pprint(request.FILES['img_prod'])
                    dir = str(loja.id)+"/produtos"


                    cloudinary.uploader.upload(rf['img_prod'], folder=dir)
                    np = new_pro.save()
                    print('vincula Insumos')
                    pprint(cont)
                    for p in cont:
                        pprint(p)
                        prodins = models.Insumos.objects.get(pk= p,loja=loja)
                        prodins.produto_prod = np
                        prodins.save()
                    print('produto criado')
                    pprint(new_prod)
                    messages.success(request, "Produto cadastrado !")
                    return redirect('administrador')
                else:
                    messages.warning(request, "Dados inválidos !")

            if 'relator' in rq:

                if len(rq) <5 and rq['date_ate'] == '' and rq['date_de'] == '':
                    messages.warning(request, "Sem dados para conulta !")

                # comandas
                if rq['relator'] == 'relacomanda':

                    result = models.Comanda.objects.get(loja=loja)

                    # filtros
                    if rq['nmesa_comanda'] != '':
                        result = result.filter(
                            n_mesa=rq['nmesa_comanda']
                        )
                    if rq['nome_comanda'] != '':
                        result = result.filter(
                            nome=rq['nome_comanda']
                        )
                    if rq['date_de'] != '':
                        result = result.exclude(
                            data =datetime.datetime.strptime(rq['date_de'], '%Y-%m-%dT%H:%M')
                        )

                    if rq['date_ate'] != '':
                        result = result.filter(
                            data =datetime.datetime.strptime(rq['date_ate'], '%Y-%m-%dT%H:%M')
                        )

                    if 'cat_comanda' in rq and rq['cat_comanda'] != '':
                        result = result.order_by(rq['cat_comanda'])

                    if 'status_comanda' in rq and rq['status_comanda'] != '':
                        result = result.filter(status= rq['status_comanda'])

                    # if rq['nmesa_comanda'] == '' and rq['nome_comanda'] == '' and rq['date_de'] == '' and rq['date_ate'] == '':
                    #     result = models.Comanda.objects.all()
                    val = 0
                    for a in result:
                        val += a.valor
                # pedidos
                elif rq['relator'] == 'relaped':
                    if len(rq) < 5 and rq['date_ate'] == '' and rq['date_de'] == '':
                        messages.warning(request, "Sem dados para conulta !")
                    result = models.Pedido.objects.get(loja=loja)
                    if rq['date_de'] != '':
                        result = result.exclude(
                            data =datetime.datetime.strptime(rq['date_de'], '%Y-%m-%dT%H:%M')
                        )

                    if rq['date_ate'] != '':
                        result = result.filter(
                            data =datetime.datetime.strptime(rq['date_ate'], '%Y-%m-%dT%H:%M')
                        )
                    if rq['nmesa_comanda'] != '':
                        result = result.filter(comandaref__n_mesa__contains = rq['nmesa_comanda'])
                    if rq['nome_comanda'] != '':
                        result = result.filter(comandaref__nome__contains = rq['nome_comanda'])
                    if 'cat_comanda' in rq and rq['cat_comanda'] != '':
                        result = result.order_by(rq['cat_comanda'])
                    if 'statsped[]' in rq and rq['statsped[]'] != '':
                        pprint(rq['statsped[]'])
                        re = rq.getlist('statsped[]')
                        pprint(re)
                        result = result.filter(status__in=rq['statsped[]'])
                        # for i in re:
                        #     print('do status', i)
                    val=0
                    for a in result:
                        val += a.valor


                # produtos
                elif rq['relator'] == 'relaprod':
                    if len(rq) < 5 and rq['date_ate'] == '' and rq['date_de'] == '':
                        messages.warning(request, "Sem dados para conulta !")
                    result = models.Produtocad.objects.get(loja=loja)
                    if rq['date_de'] != '':
                        result = result.exclude(
                            data =datetime.datetime.strptime(rq['date_de'], '%Y-%m-%dT%H:%M')
                        )

                    if rq['date_ate'] != '':
                        result = result.filter(
                            data =datetime.datetime.strptime(rq['date_ate'], '%Y-%m-%dT%H:%M')
                        )
                    if 'selec_produto[]' in rq and rq['selec_produto[]'] != '':
                        re = rq.getlist('selec_produto[]')
                        pprint(re)
                        result = result.filter(pk__in=re)
                    if 'tipo_prod' in rq and rq['tipo_prod'] != '':
                        if rq['tipo_prod'] == 'valor':

                            result = result.order_by('preco')
                        else:
                            result = result.order_by(rq['tipo_prod'])
                    if 'cat_comanda' in rq and rq['cat_comanda'] != '':
                        result = result.filter(tipo__in=rq['cat_comanda'])
                    pprint(result)
                    val = 0
                    for a in result:
                        val += a.preco
                # recebimentos
                elif rq['relator'] == 'relareceb':
                    result = models.Pagamentos.objects.get(loja=loja)
                    if len(rq) < 5 and rq['date_ate'] == '' and rq['date_de'] == '':
                        messages.warning(request, "Sem dados para conulta !")

                    if rq['date_de'] != '':
                        result = result.exclude(
                            data =datetime.datetime.strptime(rq['date_de'], '%Y-%m-%dT%H:%M')
                        )
                        pprint(result)
                        print('nodate')
                    if rq['date_ate'] != '':
                        result = result.filter(
                            data =datetime.datetime.strptime(rq['date_ate'], '%Y-%m-%dT%H:%M')
                        )
                    val=0
                    for a in result:
                        val += a.valor
                req = loja.movimento
                print('relatoriopae')
                return render(request, 'relatorio.html', {
                                                    'relatorio': result,
                                                    'logado': get_user(request),
                                                    'tp': rq['relator'],
                                                    'mov': req,
                                                    'val':val

                                                    })

            if 'cardapio' in rq:
                prod = models.Produtocad.objects.get(pk=request.POST['produto'], loja=loja)
                pprint(prod)
                if(rq['cardapio'] == '1'):
                    # print(' produto foi par ao cardapio')
                    # pprint(prod.cardapio)
                    prod.cardapio = False
                    prod.save()
                    return 1
                    # models.Produtocad.objects.filter(pk=request.POST['produto']).update(cardapio=False)
                elif(rq['cardapio'] == '0'):
                    # print(' produto saiu do cardapio')
                    # pprint(prod.cardapio)
                    prod.cardapio = True
                    prod.save()
                    return 1
                    # models.Produtocad.objects.filter(pk=request.POST['produto']).update(cardapio=True)


            if 'estoque' in rq:
                prod = models.Produtocad.objects.get(pk=rq['produto'], loja=loja)
                prod.quantidade = int(rq['estoque'])
                prod.save()
                return prod
        else:



            rq = loja.movimento
            # estado_mov = models.movi.objects.filter(pk=1)
            # print(rq)

            return render(request, 'adm.html', {'form': forms.produto,
                                                'prod': models.Produtocad.objects.filter(loja=loja),
                                                'logado': get_user(request),
                                                'mov': rq
                                                })
    else:
        messages.danger(request, "Você não tem permissão para acessar esta página.")
        return redirect('index')
# Create your views here.
