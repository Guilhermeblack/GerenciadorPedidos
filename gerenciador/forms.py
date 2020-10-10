from django import forms
from django.contrib.auth import get_user

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
        fields = 'nome','descricao','preco','tipo'

    nome = forms.CharField()
    descricao = forms.CharField()
    # preco = forms.DecimalField(decimal_places=2)
    tipo = forms.ChoiceField(choices=(
        ("A", "Alimento"),
        ("B", "Bebida"),
    ))



class pedidos(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = 'comandaref','observacao','produtosPed','quantidade','status'
        name= 'soupedido'

        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3, 'cols': 27}),
            'produtosPed': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            # 'date': forms.HiddenInput()
        }

class comandas(forms.ModelForm):

    class Meta:
        model = models.Comanda
        fields = 'nome',"n_mesa"
        name = 'soucomanda'

    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'cliente'})),
    widgets = {

    }


class mov(forms.ModelForm):

    class Meta:

        model = models.movi
        fields = {'movimento'}
        name = 'alteraMov'

