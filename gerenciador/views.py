from datetime import date
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect
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
                    return redirect('feed.html')
                elif 'cozinha' == grupo:
                    if request.user.has_perm('pedido_pronto'):
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

                messages.error(request, "erro nos grupos")
                print('cagao')
                return redirect('loguin')
# >>>>>>> a710f4bdd3c7ff0c989513e622f65bad79f492cc
            messages.error(request, 'Dados inválidos')
            return redirect('loguin')
        messages.error(request, 'Formulrio inválido')
        return render(request, 'loguin.html')
    else:
        return render(request, 'loguin.html',{'form': forms.autForm})



# descontinuar cardapio
# def cardapio(request):
#     if request.user.is_authenticated != True:
#         messages.info(request, 'Visitante. \n Data: {}'.format(date.today()))
#     else:
#         messages.info(request, 'Usuário registrado. \n Data: %s', (date.today()))
#
#     return render(request, 'cardapio.html', {'prod': models.Produtocad.objects.all()})
# >>>>>>> a710f4bdd3c7ff0c989513e622f65bad79f492cc


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
        messages.success(request, "{}, Data {}".format( 'usuario', date.today() ))
        formComanda = forms.comandas
        return render(request, 'pedidos.html', {'newcomanda': formComanda, 'prod': models.Produtocad.objects.all()})


def adm(request):
    messages.success(request, "Bem vindo Gerente ! Data {}".format(date.today()))
    return render(request, 'adm.html', {})
# >>>>>>> a710f4bdd3c7ff0c989513e622f65bad79f492cc


# Create your views here.
