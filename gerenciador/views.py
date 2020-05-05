from django.shortcuts import render
from . import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import permission_required, login_required

def index(request):
    return render(request, 'index.html',{})

def loguin(request):
    if request.POST:
        formu = form.autForm(request.POST)
        if formu.is_valid():
            username = formu.cleaned_data.get('nome')
            password = formu.cleaned_data.get('senha')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # message.succes('logado !')
                # separar mensagem para cada user group
                grupo = request.user.groups.all()
                if 'garçom' in grupo:
                    return render(request, 'pedidos.html')
                elif 'cozinha' in grupo:
                    return render(request,'feed.html')
                elif 'caixa' in grupo:
                    return render(request, 'pedidos.html')
        return render(request, 'loguin.html')
    else:
        return render(request, 'loguin.html')


def cardapio(request):
    return render(request, 'cardapio.html',{'prod': models.Produto.objects.all()})


@login_required()


def logout(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'index.html')

def feed(request):
    if user.has_perm('fazer_pedido'):
        return render(request, 'feed.html')

def ped(request):
    return render(request, 'pedidos.html')




# Create your views here.
