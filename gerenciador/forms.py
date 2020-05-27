from django import forms

from . import models


class autForm(forms.ModelForm):

    class Meta:
        model = models.logform
        fields = ('nome', 'senha')

    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'nome'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}))


class produto(forms.ModelForm):

    class Meta:
        model = models.Produtocad
        fields = 'nome','descricao','preco'

    nome = forms.CharField()
    descricao = forms.CharField()
    preco = forms.FloatField()


class pedidos(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = 'quantidade','observacao','status'
        name= 'soupedido'



class comandas(forms.ModelForm):

    class Meta:
        model = models.Comanda
        fields = 'nome',"n_mesa"
        name = 'soucomanda'
