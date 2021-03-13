from django import forms
from django.contrib.auth import get_user
from . import models
import cloudinary

class autForm(forms.ModelForm):

    class Meta:
        model = models.logform
        fields = ('nome', 'senha')

    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'nome'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}))


class produto(forms.ModelForm):

    class Meta:
        model = models.Produtocad
        fields = 'nome','descricao','preco','tipo','img_prod','quantidade','medida','cardapio','qnt_minima'

        widgets = {
            'descricao' : forms.Textarea(attrs={'rows': 3, 'cols': 27})

        }

class pedidos(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = 'comandaref','produtosPed','observacao','quantidade','status','valor'
        name= 'soupedido'

        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3, 'cols': 27}),
            # 'produtosPed': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'valor': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(pedidos, self).__init__(*args, **kwargs)
        self.fields['produtosPed'].label =''

class comandas(forms.ModelForm):

    class Meta:
        model = models.Comanda
        fields = 'nome',"n_mesa"
        name = 'soucomanda'

    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'cliente'})),
    # valor= forms.FloatField(widget=forms.HiddenInput())


class mov(forms.ModelForm):

    class Meta:

        model = models.movi
        fields = {'movimento'}
        name = 'alteraMov'

