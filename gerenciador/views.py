from datetime import date
import datetime

import cloudinary
# import django_pagarme
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
from asgiref.sync import async_to_sync


def index(request):
    if request.user.is_anonymous :
        messages.info(request, 'Bem vindo visitante.  \n Data: {}'.format(date.today()))
    else:
        messages.info(request, 'Bem vindo {}.  \n Data: {}'.format(request.user, date.today()))
    return render(request, 'index.html')



def sobre_gb(request):
    return render(request, 'sobre_gb.html', {
        'user': request.user,
    })  # enviar para as informações da equipe de dev


def sobre(request):
    return render(request, 'sobre.html', {
        'user': request.user,
    })  # enviar para as orientações do sistema

@csrf_protect
def loguin(request):

    if request.POST:
        pprint(request.POST)
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

        if request.user.is_authenticated :
            # pprint(request.user)
            # pprint(request.user.id)

            nc = models.Newcli.objects.get(user=request.user)
            pprint(nc)
            if nc is not None:
                loja = nc.loja
            else:
                nc = models.Newcli.objects.get(user=request.user.id)
                # print('memo ???')
                loja = nc.loja

            nl = models.Newcli.objects.filter(loja = loja)
            # print('oclii')
            pprint(nl)
            # pprint(Permission.objects.filter(user= request.user))
            # pprint(request.user.get_group_permissions() )
            gp= Group.objects.filter(user=request.user)



            if 'gerenciador.iniciar_movimento' in request.user.get_group_permissions() :
                return render(request, 'loguin.html', {
                    # trazer os usuarios dessa loja
                    'cad': nl,
                    'form': forms.autForm

                })
            return redirect('profile')

        return render(request, 'loguin.html', {'form': forms.autForm})


#novo gerente e loja, controle de cadastros
@csrf_protect
def new(request):

    if request.user.is_authenticated:
        nc = models.Newcli.objects.get(user=request.user)
        loja = nc.loja
    else:
        pass

    if request.POST:
        pprint(request.POST)
        if request.user.is_authenticated:
            gp = Group.objects.get(name=request.POST['grupocli'])
        else:
            gp = 1
        # print(' --- ')
        # pprint(gp)
        # print('post da loja')

        #cria loja

        lj = forms.Newloja(request.POST )
        # pprint(lj)
        #preciso de uma loja, se nao for uma nova pego a loja do usuario logado

        if lj.is_valid():
            # pprint(lj)
            lojinha = lj.save()

        else:
            nl = models.Newcli.objects.get(user=request.user)
            lojinha = nl.loja
        gr = request.POST
        senha = gr['password']
        gr._mutable = True
        gr['password'] = make_password(senha)
        gr._mutable = False
        pprint(gr)
        ger = forms.Newcli(data=gr or None)

        pprint(ger.errors)
        if ger.is_valid():
            print('bateeu')


            # pprint(lojinha)
            gerente = ger.save(commit= False)
            gerente.loja = lojinha

            # gerente.save(commit= False)
            print(' nodaleee ')
            gerente.loja = lojinha
            gerente.save()
            gerente.groups.add(gp)

            # pprint(gerente)
            cli = models.Newcli.objects.create(user=gerente, loja=lojinha)
            cli.save()
            pprint(cli)
            # gp.save()
            # print('salvo tudo')
            if request.user.is_authenticated:

                messages.info(request, 'Bem vinda(o), fique a vontade. \n --  {}'.format(date.today()))

            else:

                # pprint(ger.cleaned_data.get('username'))
                # pprint(ger.cleaned_data.get('password'))
                # pprint(senha)
                # pprint(check_password(ger.cleaned_data.get('password'),encoded=pbkdf2_sha256))

                # password = make_password(formu.cleaned_data.get('senha'), salt=None, hasher='pbkdf2_sha256')
                username = ger.cleaned_data.get('username')

                # print(password)
                user = authenticate(
                    username=username,
                    password=senha
                )


                if user is not None and 'gerente' not in gerente.groups.all():
                    login(request, user)
                    messages.info(request, 'Bem vinda(o), aproveite o melhor sistema. Sua loja foi criada ! \n --  {}'.format(date.today()))
                    return redirect(settings.LOGIN_REDIRECT_URL, permanent=True)

        else:
            lojinha.delete()
            messages.info(request, 'Cadastro inválido. Loja Não criada \n --  {}'.pprint(ger.errors))


            # user = User.objects.create_user(request.POST['Usuario'], request.POST['Email'], request.POST['Senha'] )
            # user.first_name = request.POST['Nome']
            # user.last_name = request.POST['Sobrenome']
            # user.has_perm('gerente.add_bar')
            # user.permissions.set(['fazer_pedido', 'ver_feed','iniciar_movimento','fechar_comanda','abrir_comanda','controlar_produtos'])
            #
            # user.groups.add(gp)
            # user.save()

            # pprint(gerente)

    else:
        if request.user.is_anonymous:
            grups = [1,3,5]

        else:
            grups = Group.objects.all()
    grups = Group.objects.all()
    return render(request, 'newcliente.html',{
        'loja': forms.Newloja,
        'clie': forms.Newcli,
        'groups': grups
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


@permission_required('gerenciador.ver_feed')
def feed(request):
    nc = models.Newcli.objects.get(user=request.user)
    loja = nc.loja

    # pprint(loja)
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
        # EXCLUIR/ CANCELAR PEDIDOS
        if 'exc_ped' in request.POST:
            pprint(request.POST)
            ped = models.Pedido.objects.get(pk=request.POST['exc_ped'])
            ped.status="C"
            ped.valor =0
            # pprint(ped)
            # pprint(ped.produtosPed.all())
            produto_ped = models.Produtocad.objects.get(pk=ped.produtosPed.all()[0].id)

            comanda = models.Comanda.objects.get(pk=ped.comandaref.id)
            vll = ped.quantidade *produto_ped.preco
            # print(vll, '  <<< vll')
            # comanda.valor -= vll

            # em caso de pedido cancelado eu retorno as quantidades de insumo ao estoque
            pega_prod = models.Insumos.objects.filter(produto_prod=produto_ped, loja=loja)
            for ins in pega_prod:
                pprint(ins.insumo_prod)
                ins.insumo_prod.quantidade = ins.insumo_prod.quantidade + ins.quantidade_prod
                ins.insumo_prod.save()

            comanda.save()
            ped.save()
            # o produto recebe de volta sua quantidade de acorco com pedido


            # os Insumos recebem de volta sua quantidade conforme o que é usado no produto vezes quantidade do produto
            messages.success(request, "{}, Pedido cancelado com sucesso!".format(request.user))

        # FEITA A ALTERAÇÃO DO STATUS DO PEDIDO
        if 'stats' in request.POST:
            # print(request.POST)
            ped= models.Pedido.objects.get(pk=request.POST['idstat'])
            # pprint(ped)
            ped.status=request.POST['stats']
            ped.save()
            messages.success(request, "{}, status alterado com sucesso.".format(request.user))
            # return render(request, 'feed.html', {
            #
            #     'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
            #     'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id'),
            #     'choices': STATUS_CHOICES,
            #     'fpg': FORMA_PGT,
            #     'movi': estado_mov
            # })

        # REALIZANDO OPAGAMENTODE PRODUTOS DO PEDIDO
        if 'comanda_x' in request.POST:
            # tirar do total da comanda

            pprint(request.POST)

            com = models.Comanda.objects.get(pk=int(request.POST['comanda_x']),loja=loja)
            valo_ped = float(request.POST['valo'])

            # loop itens

            valo= valo_ped
            if 'pedi[]' in request.POST:
                peed = request.POST['pedi[]']
                # pprint(peed)
                # print('entao foi o pedd')

                if isinstance(peed, str):
                    pedido_prod = models.Pedido.objects.get(pk=peed)
                    print('apenas um item sendo pago')
                    pprint(pedido_prod)
                    com.valor -= valo_ped
                    if valo >= pedido_prod.valor:
                        if com.valor <= 0:
                            com.status = "F"
                            receb = models.Pagamentos.objects.create(
                                valor=float(valo_ped),
                                status="F",
                                loja= loja
                            )

                            # nc = models.Newcli.objects.get( com.cliente)
                            # pprint(nc)
                            # models.User.objects.get(pk=com.cliente.user).delete()
                            com.cliente.user.delete()
                            com.cliente.delete()
                            # pprint(com)
                            # print('comandinha ')
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
                            loja=loja
                        )
                        receb.pedidored.add(pedido_prod)
                        receb.save()
                        com.save()
                        pedido_prod.save()
                        pass

                    else:

                        if valo > 0:
                            print('valor nao paga produto sobra {} '.format(pprint(valo)))
                            print(valo,'  valoo')
                            pedido_prod.valor -= valo
                            print(com.valor,'  comanda valoor')
                            print(pedido_prod.valor,'  valor do pedido')
                            pedido_prod.status_pago = "R"
                            receb = models.Pagamentos.objects.create(
                                valor=valo_ped,
                                status="R",
                                loja=loja
                            )
                            receb.pedidored.add(pedido_prod)
                            receb.save()
                            pedido_prod.save()
                            com.save()
                            print('passo aqui')
                            pass


                    pedido_prod.save()
                    new_status = 'ATUALIZADA com sucesso'
                    pass

                elif peed.length > 0:
                    pprint('mais de um produto no pedido')
                    com.valor -= valo_ped
                    for num, p in peed:
                        pprint('loop dos produtos sendo pagos')
                        pprint(p)
                        pedido_prod = models.Pedido.objects.get(pk=p)
                        pprint(pedido_prod)
                        if valo >= pedido_prod.produtosPed.all()[0].preco:
                            print('valor sendo pago {}  é maior que valor do produto {}'.format(valo,pedido_prod.produtosPed.all()[0].preco ))
                            valo -= pedido_prod.produtosPed.all()[0].preco * pedido_prod.produtosPed.all()[0].quantidade
                            pedido_prod.valor -= valo
                            pedido_prod.status_pago = "P"
                            receb = models.Pagamentos.objects.create(
                                valor=valo_ped,
                                status="P",
                                loja=loja
                            )
                            receb.pedidored.add(pedido_prod)
                            receb.save()
                            pedido_prod.save()
                            pass
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
                                    loja=loja
                                )
                                receb.pedidored.add(pedido_prod)
                                receb.save()
                                pedido_prod.save()
                                pass
                            elif valo <= 0:


                                print('fecho o valor do pedido {}'.format(valo))
                                com.save()
                                return render(request, 'feed.html', {

                                    'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
                                    'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id'),
                                    'choices': STATUS_CHOICES,
                                    'fpg': FORMA_PGT,
                                    'movi': estado_mov
                                })
                    new_status = 'ATUALIZADA com sucesso'
                    pedido_prod.save()
                    com.save()
                    pass


                if com.valor <= 0:

                    com.status="F"
                    if com.valor <= 0:
                        com.status = "F"
                        receb = models.Pagamentos.objects.create(
                            valor=valo_ped,
                            status="F",
                            loja=loja
                        )
                        receb.pedidored.add(pedido_prod)
                        receb.save()
                        com.save()
                        nc = models.Newcli.objects.get(com.cliente)
                        models.User.objects.get(nc).delete()
                        nc.delete()
                        com.save()
                        new_status = 'FECHADA'
                        messages.success(request, "{}, Comanda {} .".format(request.user, new_status))
                        return render(request, 'feed.html', {

                            'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
                            'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id'),
                            'choices': STATUS_CHOICES,
                            'fpg': FORMA_PGT,
                            'movi': estado_mov
                        })
                    com.save()
                    new_status = 'FECHADA'
                    messages.success(request, "{}, Comanda {} .".format(request.user, new_status))
                    return render(request, 'feed.html', {

                        'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
                        'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id'),
                        'choices': STATUS_CHOICES,
                        'fpg': FORMA_PGT,
                        'movi': estado_mov
                    })
            else:
                new_status = 'Sem pedido Selecionado'
                return render(request, 'feed.html', {

                    'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
                    'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id'),
                    'choices': STATUS_CHOICES,
                    'fpg': FORMA_PGT,
                    'movi': estado_mov
                })


            messages.success(request, "{}, Comanda {} .".format(request.user, new_status))

        return render(request, 'feed.html', {

            'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
            'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id'),
            'choices': STATUS_CHOICES,
            'fpg': FORMA_PGT,
            'loja': loja.nome_loja,
            'movi': estado_mov
        })

    else:
        if request.user.is_anonymous:
            messages.success(request, "Visitante, Data {}".format(date.today()))
        else:
            messages.success(request, "{}, Data {}".format(request.user, date.today()))

        # pprint(models.Pedido.objects.all().order_by('id'))
        return render(request, 'feed.html', {

            'comandas': models.Comanda.objects.filter(loja=loja).order_by('id', 'data'),
            'pedidos': models.Pedido.objects.filter(loja=loja).order_by('id'),
            'choices': STATUS_CHOICES,
            'fpg': FORMA_PGT,
            'loja': loja.nome_loja,
            'movi': estado_mov
        })


def ped(request):


    if request.user.is_authenticated:
        nc = models.Newcli.objects.get(user=request.user)
        # pprint(nc.loja)
        # //tennho a loja do uauario atual
        loja = nc.loja

        pprint(loja)
        estado_mov = loja.movimento
        if loja.id == 1:
            produtos = models.Produtocad.objects.filter().all
            comandas = models.Comanda.objects.filter(loja=loja)
            # pprint(comandas)
        else:
            produtos = models.Produtocad.objects.filter(loja = loja)
            comandas = models.Comanda.objects.filter(loja=loja)
            pprint(comandas)


    else:
        produtos = models.Produtocad.objects.filter().all
        pprint(produtos)
        comandas= models.Comanda.objects.filter(status="A")
        estado_mov = 'L'
        loja = models.Loja.objects.get(pk=1)



    formComanda = forms.comandas
    if request.POST:
        pprint(request.POST)


        if 'n_mesa' in request.POST:
            usr = get_user(request)

            pprint(request.POST)

            # if usr.has_perm('abrir_comanda'):
            formcom = forms.comandas(request.POST)

            # pprint(formcom)

            # criar verificação do numero da comanda se nao esta aberta para nao repetir numero

            # print('tem perm')


            if formcom.is_valid():
                formco = formcom.save(commit=False)
                formco.loja = loja
                password = ""+request.POST['nome']+request.POST['n_mesa']+""
                user_comanda = models.User.objects.create_user(
                    username=request.POST['nome']+request.POST['n_mesa'],
                    password=password,
                    email= request.POST['nome']+"@mail.com"
                )



                user_comanda.groups.add(Group.objects.get(name='cliente'))
                user_comanda.save()

                userc = authenticate(
                    username=request.POST['nome']+request.POST['n_mesa'],
                    password=password
                )

                if userc is not None and request.user.is_anonymous :
                    login(request, userc)

                clientec = models.Newcli.objects.create(
                    user = user_comanda,
                    loja = loja

                )
                clientec.save()
                formco.cliente = clientec
                formco.save()

                #prgar a loja certa para filtrar os produtos


                messages.success(request, "Comanda aberta ! \n Acesso: {}".format(request.POST['nome']+request.POST['n_mesa']))
                return render(request, 'pedidos.html',
                              {'newcomanda': formComanda,
                               'prod': models.Produtocad.objects.filter(loja=loja),
                               'movi':estado_mov,
                               'comandas': models.Comanda.objects.filter(status="A",loja=loja),
                               'pedido': forms.pedidos
                               })
            else:

                messages.warning(request, "Formulário inválido! {}".pprint(formcom.errors))

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
            pprint(newped)
            if newped.is_valid():
                messag =''
                add_comanda = models.Comanda.objects.get(pk=request.POST['comandaref'])
                prod = models.Produtocad.objects.get(pk=request.POST['produtosPed'])

                qnt = int(request.POST['quantidade'])
                # print(newped)
                #verifico se o produto tem a quantidade para poder ser feito pedido
                if prod.quantidade != None and prod.qnt_minima != None and abs(prod.quantidade) :
                    if prod.quantidade > 0 and prod.quantidade > prod.qnt_minima:
                        print('vou tirar {} do produto que é {}'.format(newped.cleaned_data['quantidade'],prod.quantidade))
                        prod.quantidade -= qnt
                        if prod.quantidade <= prod.qnt_minima and  request.user.groups.all()[0].name == 'gerente':
                            messag = " Quantidade mínima do(a) {} atingido. Reabasteça o estoque".format(prod.nome)
                            messages.warning(request, messag)
                            prod.cardapio = False
                        prod.save()
                    else:
                        messag = " Estoque do(a) {} insuficiente. Reabasteça o estoque".format(prod.nome)
                        messages.warning(request, messag)
                        prod.cardapio = False
                        prod.save()

                valu = prod.preco * qnt
                newped.cleaned_data['valor'] =float(valu)
                newped['valor'].value = valu
                # print(newped.cleaned_data, '  <<<')
                if newped.is_valid():
                    j = newped.save(commit=False)
                    j.loja = prod.loja
                    j.save()
                    j.produtosPed.add(prod)


                    pega_prod = models.Insumos.objects.filter(produto_prod= prod,loja=loja)
                    # result.filter(tipo__in=rq['cat_comanda'])
                    pprint(pega_prod)
                    for ins in pega_prod:
                        # verifico se o insumo tem a quantidade para poder ser feito pedido
                        if ins.insumo_prod.quantidade > 0:
                            print(ins.quantidade_prod, ' - quantidade a tirar')
                            print(ins.insumo_prod.quantidade,' - quantidade produto')
                            ins.insumo_prod.quantidade = ins.insumo_prod.quantidade - ins.quantidade_prod
                            if ins.insumo_prod.quantidade < ins.insumo_prod.qnt_minima and request.user.groups.all()[0].name == 'gerente':
                                print('pegou um negativo')
                                ins.insumo_prod.cardapio= False
                                ins.insumo_prod.save()
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
                    ped_val = models.Pedido.objects.get(pk=j.id)
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
        if request.user.is_anonymous:
            messages.success(request, "Visitante, Data {}".format( date.today()))
        else:
            messages.success(request, "{}, Data {}".format(request.user, date.today()))
        return render(request, 'pedidos.html', {
            'newcomanda': formComanda,
            'prod': produtos,
            'comandas': comandas,
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

                models.Produtocad.objects.get(pk=request.POST['prod_x']).delete()
                estado_mov = loja.movimento
                messages.info(request, "Produto deletado com sucesso!")
                return render(request, 'adm.html', {'form': forms.produto,
                                                    'prod': models.Produtocad.objects.filter(loja=loja),
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
                else:
                    rf = 'not'
                nprod = rq
                # Insumos = rq['qnt_ins[]']
                # pprint(nprod)
                cont=[]
                nprod._mutable = True

                # breakpoint(rq)
                if 'cardapio' not in nprod:
                    nprod['cardapio'] = False
                if(nprod['cardapio'] == 'on'):
                    nprod['cardapio'] = True
                else:
                    nprod['cardapio'] = False
                nprod._mutable = False

                new_prod = forms.produto(nprod, request.FILES)

                pprint(new_prod)

                # print(new_prod.errors)
                if new_prod.is_valid():

                    new_pro =new_prod.save(commit=False)

                    new_pro.loja = loja
                    for p in list(rq):
                        if p.isnumeric():
                            # print('enumero')
                            epc = float(rq[p].replace(',', '.'))
                            print(epc)

                            print(p)
                            ins = models.Insumos.objects.create(
                                quantidade_prod=epc,
                                insumo_prod=models.Produtocad.objects.get(pk=p),

                                loja=loja

                            )
                            ins.save()
                            cont.append(ins.id)
                            nprod._mutable = True
                            nprod.pop(p)
                            nprod._mutable = False
                    # pprint(request.FILES['img_prod'])
                    if not rf == 'not':
                        dir = str(loja.id)+"/produtos"


                        cloudinary.uploader.upload(rf['img_prod'], folder=dir)
                    np = new_pro.save()
                    print('vincula Insumos')
                    pprint(new_pro)
                    for p in cont:
                        print('{} savees'.format(p))
                        prodins = models.Insumos.objects.get(pk= p)
                        prodins.produto_prod = new_pro
                        print('esse malditp {} '.format(prodins.produto_prod))
                        svp = prodins.save()
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

                    result = models.Comanda.objects.filter(loja=loja)

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
                    result = models.Pedido.objects.filter(loja=loja)
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
                    result = models.Produtocad.objects.filter(loja=loja)
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
                    result = models.Pagamentos.objects.filter(loja=loja)
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
                prod = models.Produtocad.objects.get(pk=request.POST['produto'])
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
                prod = models.Produtocad.objects.get(pk=rq['produto'])
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


def cliente(request):

    if request.POST:
        pass

    if request.user.is_authenticated:

        # //  FUNCIONARIO NAO POSSUI COMANDA
        nc = models.Newcli.objects.get(user=request.user)
        val = 0

        comanda = models.Comanda.objects.filter(cliente=nc)

        if comanda:
            # pprint(comanda)
            loja = comanda[0].loja
            pedidos = models.Pedido.objects.filter(comandaref = comanda[0])

            for p in pedidos:
                val = val+ p.valor
            pag = models.Pagamentos.objects.filter(pedidored__in = pedidos)
        else:
            comanda = []
            pedidos= []
            pag = []

    # comanda, produtos, loja
    return render(request, 'cliente.html',{
        'comanda': comanda,
        'pedidos': pedidos,
        'pag': pag,
        'val':val
    })

# Create your views here.
