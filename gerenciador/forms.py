from django import forms
from django.contrib.auth import get_user
from . import models
import cloudinary

class autForm(forms.ModelForm):

    class Meta:
        model = models.logform
        fields = ('nome', 'senha')

    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'nome'}), help_text="Insira o nome ou identificação do usuário")
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}), help_text="Insira a senha do usuário")


class produto(forms.ModelForm):

    class Meta:
        model = models.Produtocad
        fields = 'nome','descricao','preco','tipo','img_prod','quantidade','medida','cardapio','qnt_minima'

        widgets = {
            'descricao' : forms.Textarea(attrs={'rows': 3, 'cols': 27}),

            # 'nome' : forms.CharField(help_text="Este campo representa o nome do produto"),
            # 'preco' : forms.FloatField(help_text="Insira o preço do produto neste campo"),
            # 'tipo' : forms.CharField(help_text="Escolha se o produto é um alimento ou uma bebida"),
            # 'quantidade' : forms.IntegerField(widget=forms.PasswordInput(attrs={'min_value':1, 'width':15, 'require': False}) )
            # 'medida' : forms.CharField(help_text="Escolha a unidade de medida do produto"),
            # 'cardapio' : forms.BooleanField(help_text="Defina se o produto irá aparecer no cardápio"),
            # 'qnt_minima' : forms.FloatField(help_text="Defina qual a quantidade minima do produto a loja poderá ter em estoque antes de ser alertada")
        }

class pedidos(forms.ModelForm):

    class Meta:
        model = models.Pedido
        fields = 'comandaref','produtosPed','observacao','quantidade','status','valor'
        name= 'soupedido'

        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3, 'cols': 27}),
            # 'produtosPed': forms.HiddenInput(),
            # 'quantidade': forms.IntegerField(help_text="Insira a quantidade do produto que será pedido"),
            # 'comandaref': forms.SelectMultiple(help_text="Insira a quantidade do produto que será pedido"),
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

    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'cliente'}), help_text="Insira o nome da nova comanda"),
    # n_mesa = forms.IntegerField(help_text="Insira o nome da nova comanda")
    # valor= forms.FloatField(widget=forms.HiddenInput())





class Newloja(forms.ModelForm):
    class Meta:
        model = models.Loja
        fields = 'nome_loja',"porte"
        name = 'souloja'

    nome_loja : forms.CharField(help_text="Defina se o produto irá aparecer no cardápio")
    porte : forms.ChoiceField()

class Newcli(forms.ModelForm):
    class Meta:
        model = models.User
        fields = 'username', 'password', 'email', 'first_name', 'last_name'
        name = 'sounovocli'

    # username : forms.CharField(help_text="Defina o nome de usuário")
    # # password : forms.CharField(widget=forms.PasswordInput())
    # email : forms.EmailField(help_text="Defina o email")
    # first_name : forms.CharField(help_text="Defina o primeiro nome")
    # last_name : forms.CharField(help_text="Defina o segundo nome")
